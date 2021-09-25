from lux import annotate
from typing import DefaultDict
from missions.mission import Mission
from clusters.cluster import Cluster
from missions.mission_constants import MissionConstants
import maps.map_analysis as MapAnalysis
import actuators.actuator_service as ActuatorService
import missions.mission_service as MissionService
import resources.resource_service as ResourceService


def update_cluster_missions(
    cluster: Cluster,
    game_state,
) -> DefaultDict[str, Mission]:
    '''
    This is to update cluster missions.
    Remove finished missions or missions impossible!?
    Give new missions.
    Check if resource cluster is surrounded by citytiles.
    If not, priortize that. (BUILD_CITY_TILE)
    If cluster is secured, unit moves to resource cells and
    stay standby to build if citytiles die. (CLUSTER_GUARD)
    '''

    missions = MissionService.delete_mission_without_unit(
        cluster.missions,
        cluster.units
    )

    missions = MissionService.delete_completed_missions(
        cluster.missions,
        game_state,
    )

    units_without_missions = [
        unit_id for unit_id in cluster.units if unit_id not in missions
    ]

    exposed_perimeter = cluster.exposed_perimeter
    build_mission_count = 0
    for unit_id in units_without_missions:
        if build_mission_count == len(exposed_perimeter):
            break

        missions[unit_id] = Mission(
            MissionConstants.MissionType.BUILD_CITY_TILE,
        )

        build_mission_count += 1

    units_without_missions = [
        unit_id for unit_id in cluster.units if unit_id not in missions
    ]

    guard_mission_count = 0
    for unit_id in units_without_missions:
        if guard_mission_count == len(cluster.resource_cells):
            break

        missions[unit_id] = Mission(
            MissionConstants.MissionType.CLUSTER_GUARD,
        )
        guard_mission_count += 1

    # If we have more workers than required, we release them.
    released_units = [
        unit_id for unit_id in cluster.units if unit_id not in missions
    ]

    for unit_id in released_units:
        cluster.remove_unit(unit_id)

    # If cluster resources are depleted, no use for its units.
    if len(cluster.resource_cells) == 0:
        cluster.units = []

    return missions


def negotiate_missions(
    cluster: Cluster,
    game_state,
    opponent,
    mission_type,
) -> Cluster:
    '''
    This function negotiates/assigns targets to
    all the missions of the cluster.
    If the target positions are fewer than the unit,
    some unit mission will not have target position.
    '''
    units = [
        mission.unit for _, mission in cluster.missions.items()
        if mission.mission_type == mission_type
        and mission.allow_target_overwrite
    ]

    if len(units) == 0:
        return cluster

    target_positions = []
    if mission_type == MissionConstants.MissionType.BUILD_CITY_TILE:
        target_positions = ActuatorService.get_top_positions(
            game_state,
            opponent,
            cluster.exposed_perimeter,
            cluster.missions
        )

    if mission_type == MissionConstants.MissionType.CLUSTER_GUARD:
        target_positions = ActuatorService.get_top_positions(
            game_state,
            opponent,
            [cell.pos for cell in cluster.resource_cells],
            cluster.missions
        )

    if mission_type == MissionConstants.MissionType.EXPLORATION:
        target_positions = cluster.exposed_perimeter

    if len(target_positions) == 0:
        return cluster

    missions = MissionService.negotiate_missions(
        cluster.missions,
        units,
        target_positions
    )

    cluster.missions = missions
    return cluster


def handle_explorations(
    cluster: Cluster,
    game_state_info,
    resource_cells,
    actions
):
    '''
    This function's responsibility is to prevent unit dying at night
    during long range travel to new clusters.
    If the unit does not carry enough fuel/resource to survive at night,
    we direct it to nearest resource to refill.
    '''
    for key in cluster.missions.copy():
        mission = cluster.missions[key]
        if mission.mission_type == \
                MissionConstants.MissionType.EXPLORATION and \
                mission.unit is not None:

            closest_perimeter, distance = MapAnalysis.get_closest_position(
                mission.unit.pos,
                cluster.exposed_perimeter
            )

            # This is not well thought out.
            night_turns_required = 0
            if game_state_info['is_night_time']:
                night_turns_required = distance * 4

            turns_required = distance * 2
            if turns_required > game_state_info['turns_to_night']:
                night_turns_required = turns_required - \
                    game_state_info['turns_to_night']

            night_fuel_required = night_turns_required * 4

            unit_fuel = 100 - mission.unit.get_cargo_space_left()

            # If the unit does not have enough fuel, we want it to go
            # to nearest resource to collect it.
            # Currently, this backfires if citytile is in front of it,
            # it can never leave the cluster because if he hits the citytile,
            # his/her carried resources are empty
            # so he/she will not have fuel to travel.
            if unit_fuel < night_fuel_required:
                actions.append(
                    annotate.sidetext(
                        f'{mission.unit.id} You are going to die at night'
                    )
                )
                closest_resource_cell, distance = ResourceService \
                    .get_closest_resource_tile(
                        mission.unit.pos,
                        resource_cells
                    )

                # We do not need to go to the resource cell,
                # just getting to the adjacent cell is enough
                if closest_resource_cell is not None:
                    if distance == 1:
                        mission.update_target_pos(mission.unit.pos)

                    mission.update_target_pos(closest_resource_cell.pos)
                    # This is to force non-negotiable target position.
                    # He/she needs to get resource.
                    mission.allow_target_overwrite = False
            else:
                mission.update_target_pos(closest_perimeter)
                mission.allow_target_overwrite = True

    return cluster

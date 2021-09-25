from typing import DefaultDict
from collections import defaultdict
from lux import annotate

from lux.game import Game

import actuators.actuator_controller as ActuatorController
import annotators.annotator_controller as AnnotatorController
import cities.city_controller as CityController
import clusters.cluster_controller as ClusterController
import spies.spy_controller as SpyController
from clusters.cluster import Cluster
import game_state_info.game_state_info as GameStateInfo
from missions.mission import Mission
from missions.mission_constants import MissionConstants
import missions.mission_controller as MissionController
import resources.resource_service as ResourceService
import units.unit_controller as UnitController


game_state = None
clusters: DefaultDict[str, Cluster] = defaultdict(Cluster)
game_state_info = defaultdict(dict)


def agent(observation, configuration):
    global game_state
    global clusters
    global game_state_info

    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player

        # This is the start of the game
        clusters = ClusterController.init_clusters(game_state)
    else:
        game_state._update(observation["updates"])

    actions = []

    # To update day and night information
    game_state_info = GameStateInfo.update_game_state_info(
        observation['step']
    )

    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    game_state.update_players(player, opponent)
    player_id = observation.player
    opponent_id = (observation.player + 1) % 2

    opponent_citytiles = SpyController \
        .get_opponent_citytiles(opponent)

    resource_cells = ResourceService.get_resources(game_state)
    minable_resource_cells = ResourceService.get_minable_resource_cells(
        player,
        resource_cells
    )

    # The first thing we do is updating the cluster.
    # Refer to the cluster class for its attributes.
    for k in clusters:
        clusters[k] = ClusterController.update_cluster(
            clusters[k],
            game_state,
            player,
        )

    # This is to update cluster missions.
    # Remove finished missions or missions impossible!?
    # Give new missions.
    for k in clusters:
        clusters[k].missions = MissionController.update_cluster_missions(
            clusters[k],
            game_state
        )

    # We have new born units, or units released from clusters.
    # We need to find them new home.
    units_without_clusters = ClusterController.get_units_without_clusters(
        player.units,
        clusters
    )

    for unit in units_without_clusters:
        cluster = ClusterController.assign_worker_cluster(
            unit,
            clusters,
            game_state,
            player,
            player_id,
            opponent,
            opponent_id,
        )
        if cluster is None:
            continue

        actions.append(
            annotate.sidetext(f'assign {unit.id} cluster {cluster.id}')
        )

        clusters[cluster.id].add_unit(unit.id)

        # We call them Explorers.
        clusters[cluster.id].missions[unit.id] = Mission(
            MissionConstants.MissionType.EXPLORATION
        )

    # This is just to debug.
    final_units_without_clusters = ClusterController \
        .get_units_without_clusters(
            player.units,
            clusters
        )

    if len(final_units_without_clusters) > 0:
        print(
            '>><<>><<>><< WITHOUT CLUSTER >><<>><<>><<',
            len(final_units_without_clusters)
        )

    # By this time, all units should have cluster and mission.
    # If all clusters are gone, units would not have any.
    # We need to update unit, because unit moves or its resource
    # is changed, so, the mission needs to know the unit latest status.
    for k in clusters:
        for m in clusters[k].missions:
            unit = UnitController.get_unit_by_id(m, player.units)
            clusters[k].missions[m].update_unit(unit)

    # Notice that, when we assign mission, we do not define the targets.
    # Build citytile and we do not tell where.
    # Because if more than one worker has to build citytiles,
    # it makes more sense to choose nearest to each worker.
    # The negotiation is to use Linear Sum Assignment to assign
    # the optimal locations for the workers.
    for k in clusters:
        if len(clusters[k].missions) == 0:
            continue

        clusters[k] = MissionController.negotiate_missions(
            clusters[k],
            game_state,
            opponent,
            MissionConstants.MissionType.BUILD_CITY_TILE,
        )

        clusters[k] = MissionController.negotiate_missions(
            clusters[k],
            game_state,
            opponent,
            MissionConstants.MissionType.CLUSTER_GUARD,
        )

        # Exploration missions got special treatment because
        # we would not want workers to die at night during travelling
        clusters[k] = MissionController.handle_explorations(
            clusters[k],
            game_state_info,
            minable_resource_cells,
            actions,
        )

        clusters[k] = MissionController.negotiate_missions(
            clusters[k],
            game_state,
            opponent,
            MissionConstants.MissionType.EXPLORATION,
        )

    # The action component starts here.
    # We have cluster, we have mission so, we need to carry out the missions.

    # We first find the unmovable things.
    occupied_positions = set()
    opponent_citytiles = set()
    for city in opponent.cities.values():
        for city_tile in city.citytiles:
            opponent_citytiles.add((city_tile.pos.x, city_tile.pos.y))
    occupied_positions = occupied_positions.union(opponent_citytiles)

    unable_units_positions = set()
    for unit in player.units:
        if not unit.can_act():
            unable_units_positions.add((unit.pos.x, unit.pos.y))
    occupied_positions = occupied_positions.union(unable_units_positions)

    # if unit has mission but no target, he/she will not move. So, we need
    # to include them.
    units_without_target_positions = set()
    for k in clusters:
        for _, mission in clusters[k].missions.items():
            if mission.target_pos is None:
                unit = mission.unit
                units_without_target_positions.add((unit.pos.x, unit.pos.y))
    occupied_positions = occupied_positions.union(
        units_without_target_positions
    )

    # If unit is at target, he/she will not move.
    units_at_target_positions = set()
    for k in clusters:
        for _, mission in clusters[k].missions.items():
            if mission.target_pos is not None and \
                    mission.unit is not None and \
                    mission.target_pos.equals(mission.unit.pos):
                unit = mission.unit
                units_at_target_positions.add((unit.pos.x, unit.pos.y))
    occupied_positions = occupied_positions.union(units_at_target_positions)

    # Player citytile can hold many units so the collision will not happen.
    player_citytiles = set()
    for city in player.cities.values():
        for city_tile in city.citytiles:
            player_citytiles.add((city_tile.pos.x, city_tile.pos.y))

    occupied_positions = occupied_positions.difference(player_citytiles)

    for k in clusters:
        if len(clusters[k].missions) == 0:
            continue

        actions.extend(
            ActuatorController.get_build_actions(clusters[k], game_state_info)
        )

    # We want to get all the movements requested for all the units.
    requested_movements = []
    for k in clusters:
        requested_movements.extend(
            ActuatorController.get_cluster_movement(clusters[k])
        )

    # We call the shots. Who go and who do not
    negotiated_actions = ActuatorController.negotiate_actions(
        occupied_positions,
        requested_movements
    )

    actions.extend(negotiated_actions)

    for k in clusters:
        annotations = AnnotatorController.get_mission_annotations(
            clusters[k].missions
        )
        actions.extend(annotations)

    city_actions = CityController.get_city_actions(
        game_state,
        game_state_info,
        player,
        clusters,
        player_id,
        opponent,
        opponent_id,
    )
    actions.extend(city_actions)

    return actions

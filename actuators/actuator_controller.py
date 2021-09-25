from clusters.cluster import Cluster
from missions.mission import Mission
import actuators.actuator_service as ActuatorService
from missions.mission_constants import MissionConstants


def get_movements(
    mission: Mission,
):
    '''
    The movements that will get the unit to its target.
    '''
    unit = mission.unit
    target_pos = mission.target_pos

    directions = ActuatorService.get_all_directions(
        unit.pos, target_pos
    )

    movements = []
    for direction in directions:
        next_pos = unit.pos.translate(direction, 1)
        movements.append({
            'direction': direction,
            'next_pos': next_pos
        })

    return {
        'unit_id': unit.id,
        'unit': unit,
        'movements': movements,
        'approved': False,
        'mission': mission
    }


def negotiate_actions(occupied_positions, requested_movements):
    '''
    This is just a simple heuristics.
    We prioritize unit that has only one direction to go.
    Currently, the unit does not have intelligence to make it way around
    and obstacle. If there is an obstacle, he/she simple waits till
    the obstacle is gone. More research is needed.
    '''

    # TO-DO make it more efficient
    # SORT UNIT BY PRIORTIY HEURISTICS
    actions = []

    # unmovable_units or obstacles
    for requested_movement in requested_movements:
        for movement in requested_movement['movements']:
            if (movement['next_pos'].x, movement['next_pos'].y) \
                    not in occupied_positions:
                break

            occupied_positions.add(
                (
                    requested_movement['unit'].pos.x,
                    requested_movement['unit'].pos.y
                )
            )
            requested_movement['approved'] = False

    for requested_movement in requested_movements:
        if len(requested_movement['movements']) == 1:
            movement = requested_movement['movements'][0]
            if (movement['next_pos'].x, movement['next_pos'].y) \
                    not in occupied_positions:
                actions.append(
                    requested_movement['unit'].move(movement['direction'])
                )
                occupied_positions.add(
                    (movement['next_pos'].x, movement['next_pos'].y)
                )
                requested_movement['approved'] = True
            else:
                occupied_positions.add(
                    (requested_movement['unit'].pos.x,
                     requested_movement['unit'].pos.y)
                )

    for requested_movement in requested_movements:
        if len(requested_movement['movements']) > 1:
            movements = requested_movement['movements']
            for movement in movements:
                if (movement['next_pos'].x, movement['next_pos'].y) \
                        not in occupied_positions:
                    actions.append(
                        requested_movement['unit'].move(movement['direction'])
                    )
                    occupied_positions.add(
                        (movement['next_pos'].x, movement['next_pos'].y)
                    )
                    requested_movement['approved'] = True
                    break

        if not requested_movement['approved']:
            occupied_positions.add(
                (
                    requested_movement['unit'].pos.x,
                    requested_movement['unit'].pos.y
                )
            )

    return actions


def get_cluster_movement(cluster: Cluster):
    '''
    This function returns all the movements requested
    by all of its missions.
    '''
    movements = []

    for key in cluster.missions:
        unit = cluster.missions[key].unit
        target_pos = cluster.missions[key].target_pos

        if unit is None or target_pos is None:
            continue

        if unit.can_act() and not unit.pos.equals(target_pos):
            movements.append(
                get_movements(cluster.missions[key])
            )

    return movements


def get_build_actions(cluster: Cluster, game_state_info):
    '''
    This return build command if it is a good to build citytile.
    '''
    build_actions = []

    for key in cluster.missions:
        mission = cluster.missions[key]
        if mission.mission_type == \
                MissionConstants.MissionType.BUILD_CITY_TILE and \
                mission.target_pos is not None and \
                mission.unit.pos.equals(mission.target_pos) and \
                mission.unit.get_cargo_space_left() == 0 and \
                mission.unit.can_act() and \
                game_state_info['turns_to_night'] > 5:

            build_actions.append(mission.unit.build_city())

    return build_actions

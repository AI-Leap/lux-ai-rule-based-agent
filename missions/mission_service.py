# from clusters.cluster import Cluster
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
from typing import DefaultDict, List

from lux.game_objects import Unit
from lux.game_map import Position
from missions.mission_constants import MissionConstants
from missions.mission import Mission


def delete_mission_without_unit(missions: List[Mission], units_ids: List[str]):
    for key in missions.copy():
        if key not in units_ids:
            del missions[key]

    return missions


def delete_completed_missions(
    missions: DefaultDict[str, Mission],
    game_state
):
    for key in missions.copy():
        mission = missions[key]

        if mission.target_pos is None:
            continue

        if mission.mission_type == \
                MissionConstants.MissionType.BUILD_CITY_TILE:

            target_pos = mission.target_pos
            cell = game_state.map.get_cell_by_pos(target_pos)
            if cell.citytile is not None:
                del missions[key]

        if mission.mission_type == \
                MissionConstants.MissionType.EXPLORATION:
            if mission.unit.pos.equals(
                mission.target_pos
            ) and mission.allow_target_overwrite is True:
                del missions[key]

        if mission.mission_type == \
                MissionConstants.MissionType.CLUSTER_GUARD:
            if mission.unit.pos.equals(
                mission.target_pos
            ):
                del missions[key]

    return missions


def negotiate_missions(
    missions: DefaultDict[str, Mission],
    units: List[Unit],
    targets: List[Position],
) -> DefaultDict[str, Mission]:
    '''
    This is the function that uses linear sum assignment algorithm.
    The distance matrix is simple. We just use Mahattan distance.
    TO-DO: We can make the cost matrix more sophisticated.
    '''
    unit_positions = [(unit.pos.x, unit.pos.y) for unit in units]
    target_positions = [(target.x, target.y) for target in targets]

    def distance_to(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    distance_matrix = cdist(
        unit_positions,
        target_positions,
        distance_to
    )

    row_ind, col_ind = linear_sum_assignment(distance_matrix)
    for i in range(len(row_ind)):
        key = units[row_ind[i]].id
        target = target_positions[col_ind[i]]
        missions[key].update_target_pos(Position(target[0], target[1]))

    return missions

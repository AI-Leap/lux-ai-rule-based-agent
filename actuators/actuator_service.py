from functools import cmp_to_key
from typing import List
from lux.game_map import Position
import models.build_model as BuildModel


def get_all_directions(src: Position, dest: Position) -> List[str]:
    directions = []
    if dest.y - src.y < 0:
        directions.append('n')
    if dest.y - src.y > 0:
        directions.append('s')
    if dest.x - src.x > 0:
        directions.append('e')
    if dest.x - src.x < 0:
        directions.append('w')
    return directions


def get_top_positions(game_state, opponent, positions, missions):
    '''
    This function is to sort the positions.
    The idea is we want to build or mobilize our units closer to
    opponent units. If the new cluster is secured, we should build
    citytiles first to the side the opponents are coming.
    Much to improve this scoring.
    '''

    # this scoring needs the distance from the worker to the target.
    # However, this case is tricky, we cannot calculate of each unit.
    # So, I average the unit positions and use it to calculate.
    # TO-DO refactor to improve this part.
    sum_x = sum([
        mission.unit.pos.x for _, mission in missions.items()
        if mission.unit is not None
    ])
    sum_y = sum([
        mission.unit.pos.y for _, mission in missions.items()
        if mission.unit is not None
    ])

    average_x = sum_x / len(missions)
    average_y = sum_y / len(missions)

    units_centroid = Position(average_x, average_y)

    def compare(pos1, pos2):
        return pos2['score'] - pos1['score']

    positions_to_be_sorted = []
    for p in positions:
        score = BuildModel.get_build_pos_score(
            game_state,
            opponent,
            p,
            units_centroid,
        )
        positions_to_be_sorted.append({
            'pos': p,
            'score': score
        })

    sorted_positions = sorted(positions_to_be_sorted, key=cmp_to_key(compare))

    # We only return only the number needed.
    return [p['pos'] for p in sorted_positions][:len(missions)]

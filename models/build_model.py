import maps.map_analysis as MapAnalysis


def get_build_pos_score(game_state, opponent, pos, units_centroid):
    '''
    Returns the score of a position that the citytile is to be build.
    Needs to improve this scoring.
    Right now, it is just okay.
    '''
    travel_distance = units_centroid.distance_to(pos)
    travel_distance_score = 100 / ((travel_distance ** 2) + 1)

    opponent_distances = []
    for unit in opponent.units:
        distance = pos.distance_to(unit.pos)
        opponent_distances.append(distance)

    opponent_distance_score = (10 * len(opponent.units)) \
        / (sum(opponent_distances) + 1)

    perimeter = MapAnalysis.get_perimeter(
        [game_state.map.get_cell_by_pos(pos)],
        game_state.map.width,
        game_state.map.height
    )

    perimeter_score = 0
    for p in perimeter:
        cell = game_state.map.get_cell_by_pos(p)
        if cell.citytile is not None:
            perimeter_score += 2

    final_score = perimeter_score + opponent_distance_score \
        + travel_distance_score

    return final_score

import maps.map_analysis as MapAnalysis
import spies.spy_service as SpyService
from models.weights import Weights


def get_cluster_score(
    cluster,
    worker,
    game_state,
    player,
    player_id,
    opponent,
    opponent_id
):
    '''
    This function is calcuate the score of the cluster.
    The higher the score, the better the worker should go.
    This needs to be tuned.
    As a machine learning beginner, I expressed the function as
    expression with weights. We need biases.
    May the best weights win.
    '''
    if len(cluster.resource_cells) == 0:
        return 0

    _, distance = MapAnalysis.get_closest_position(
        worker.pos,
        cluster.exposed_perimeter,
    )

    perimeter = MapAnalysis.get_perimeter(
        cluster.resource_cells,
        game_state.map.width,
        game_state.map.height
    )
    perimeter_cells = [
        game_state.map.get_cell_by_pos(pos) for pos in perimeter
    ]

    perimeter_cells.extend(cluster.resource_cells)
    # We want to check how many units and citytiles are already
    # in the cluster and its perimeter.
    opponent_citytiles, opponent_units = SpyService.get_enemy_coverage(
        perimeter_cells,
        opponent,
        opponent_id,
    )

    # And how many of the perimeter are our citytiles.
    player_citytiles = []
    for p in perimeter:
        cell = game_state.map.get_cell_by_pos(p)
        if cell.citytile is not None:
            if cell.citytile.team == player_id:
                player_citytiles.append(cell.citytile)

    cluster_score = distance * Weights.Cluster.DISTANCE + \
        len(cluster.resource_cells) * Weights.Cluster.RESOURCE_CELLS + \
        len(perimeter) * Weights.Cluster.PERIMETER + \
        len(opponent_units) * Weights.Cluster.OPPONENT_UNITS + \
        len(opponent_citytiles) * Weights.Cluster.OPPONENT_CITYTILES + \
        len(player_citytiles) * Weights.Cluster.PLAYER_CITYTILES + \
        len(cluster.units) * Weights.Cluster.PLAYER_UNITS

    return cluster_score


def get_citytile_score(
    cluster,
    game_state,
    player_id,
    opponent,
    opponent_id
):
    '''
    A simple mathematical model to calculate a citytile should build a worker.
    '''
    # directly proportional
    resource_cell_score = len(cluster.resource_cells)
    fuel_score = cluster.get_available_fuel() / 100

    perimeter = MapAnalysis.get_perimeter(
            cluster.resource_cells,
            game_state.map.width,
            game_state.map.height
        )
    perimeter_score = len(perimeter)

    opponent_citytiles, opponent_units = SpyService.get_enemy_coverage(
        [game_state.map.get_cell_by_pos(pos) for pos in perimeter],
        opponent,
        opponent_id,
    )
    opponent_workers_score = len(opponent_units) + 1
    opponent_citytiles_score = len(opponent_citytiles) + 1

    # inversely proportional
    player_citytiles = []
    for p in perimeter:
        cell = game_state.map.get_cell_by_pos(p)
        if cell.citytile is not None:
            if cell.citytile.team == player_id:
                player_citytiles.append(cell.citytile)

    player_workers_score = 10 * len(cluster.units) + 1
    player_citytiles_score = len(player_citytiles) + 1

    no_player_unit_bonus = 10 if len(cluster.units) == 0 else 1

    numerator = resource_cell_score * fuel_score * perimeter_score * \
        no_player_unit_bonus * opponent_workers_score * \
        opponent_citytiles_score

    denominator = player_workers_score * player_citytiles_score

    citytile_score = numerator / (denominator + 1.1)

    return citytile_score

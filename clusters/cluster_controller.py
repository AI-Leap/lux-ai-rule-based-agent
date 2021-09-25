from functools import cmp_to_key
from collections import defaultdict
from typing import List, DefaultDict
from lux.game_map import RESOURCE_TYPES, Position, Cell
from lux.game_objects import Unit
import maps.map_analysis as MapAnalysis
from clusters.cluster import Cluster
import resources.resource_service as ResourceService
import models.cluster_model as ClusterModel


def init_clusters(game_state) -> DefaultDict[str, Cluster]:
    '''
    This is called only once, when the game starts.
    The cluster types are wood, coal, and uranium.
    If two resource cells are adjacent, or diagonal to each other,
    we assume they are in the same cluster.
    '''
    clusters: DefaultDict[str, Cluster] = defaultdict(Cluster)
    resource_cells = ResourceService.get_resources(game_state)

    # creating wood clusters
    wood_resource_cells = [
        resource_tile for resource_tile in resource_cells
        if resource_tile.resource.type == RESOURCE_TYPES.WOOD
    ]
    for i, rc in enumerate(
            MapAnalysis.get_resource_groups(wood_resource_cells)
    ):
        clusters[f'wood_{i}'] = Cluster(f'wood_{i}', rc)

    # creating coal clusters
    coal_resource_cells = [
        resource_tile for resource_tile in resource_cells
        if resource_tile.resource.type == RESOURCE_TYPES.COAL
    ]
    for i, rc in enumerate(
            MapAnalysis.get_resource_groups(coal_resource_cells)
    ):
        clusters[f'coal_{i}'] = Cluster(f'coal_{i}', rc)

    # creating uranium clusters
    uranium_resource_cells = [
        resource_tile for resource_tile in resource_cells
        if resource_tile.resource.type == RESOURCE_TYPES.URANIUM
    ]
    for i, rc in enumerate(
            MapAnalysis.get_resource_groups(uranium_resource_cells)
    ):
        clusters[f'uranium_{i}'] = Cluster(f'uranium_{i}', rc)

    return clusters


def update_cluster(
    cluster: Cluster,
    game_state,
    player,
) -> Cluster:
    '''
    This is to update the cluster information.
    We update resource cells because resource cells are consumed.
    Some of its assigned units (workers) may die or leave.
    We update how much of its perimeter is not guarded by citytile.

    WARNING: Most bugs I had were caused by this function. Take care
    if you change this.
    '''
    resource_cells: List[Cell] = ResourceService \
        .get_resource_cells_by_positions(
            game_state,
            [cell.pos for cell in cluster.resource_cells]
        )

    cluster.resource_cells = resource_cells

    alive_units = [
        id for id in cluster.units if id in
        [u.id for u in player.units]
    ]
    cluster.units = alive_units

    perimeter: List[Position] = MapAnalysis.get_perimeter(
        resource_cells,
        game_state.map.width,
        game_state.map.height
    )

    exposed_perimeter = [
        p for p in perimeter
        if game_state.map.get_cell_by_pos(p).citytile is None and
        not game_state.map.get_cell_by_pos(p).has_resource()
    ]
    cluster.exposed_perimeter = exposed_perimeter

    return cluster


def get_cluster_by_worker(worker: Unit, clusters: List[Cluster]) -> Cluster:
    for cluster in clusters:
        if worker.id in cluster.workers:
            return cluster

    return None


def assign_worker_cluster(
    worker: Unit,
    clusters,
    game_state,
    player,
    player_id,
    opponent,
    opponent_id
):
    clusters_to_sort = clusters.copy()
    player = game_state.player

    for key in clusters:
        if not player.researched_coal() and 'coal' in key:
            del clusters_to_sort[key]
        if not player.researched_uranium() and 'uranium' in key:
            del clusters_to_sort[key]

    cluster_scores = []
    for key in clusters_to_sort:
        cluster_score = ClusterModel.get_cluster_score(
            clusters_to_sort[key],
            worker,
            game_state,
            player,
            player_id,
            opponent,
            opponent_id,
        )
        cluster_scores.append({
            'cluster': clusters_to_sort[key],
            'score': cluster_score
        })

    def compare_final_score(c1, c2):
        return c2['score'] - c1['score']

    sorted_clusters = sorted(
        cluster_scores, key=cmp_to_key(compare_final_score)
    )

    if len(sorted_clusters) > 0:
        return sorted_clusters[0]['cluster']

    return None


def get_units_without_clusters(
    units: List[Unit],
    clusters: DefaultDict[str, Cluster]
) -> List[Unit]:

    units_with_clusters = []
    for k in clusters:
        units_with_clusters.extend(clusters[k].units)

    units_without_clusters = []
    for unit in units:
        if unit.id not in units_with_clusters:
            units_without_clusters.append(unit)

    return units_without_clusters


# def get_citytiles_without_clusters(citytiles, clusters):
#     citytiles_with_cluster = []
#     for k in clusters:
#         citytiles_with_cluster.extend(clusters[k].citytiles)

#     citytiles_without_cluster = []
#     for citytile in citytiles:
#         if unit.id not in units_with_clusters:
#             units_without_clusters.append(unit)

#     return units_without_clusters

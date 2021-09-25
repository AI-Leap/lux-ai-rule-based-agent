import math
from functools import cmp_to_key
from typing import List
from lux.game_map import Position
from clusters.cluster import Cluster


def get_closest_cluster(pos: Position, clusters) -> Cluster:
    closest_distance = math.inf
    closest_cluster = None

    for k in clusters:
        distance = pos.distance_to(clusters[k].get_centroid())
        if distance < closest_distance:
            closest_distance = distance
            closest_cluster = clusters[k]

    return closest_cluster


def sort_clusters_by_distance(
    pos: Position,
    clusters: List[Cluster]
) -> List[Cluster]:
    sorted_clusters = [cluster for _, cluster in clusters.items()
                       if len(cluster.resource_cells) > 0]

    # not always right TO-DO refactor
    def compare(cluster_a, cluster_b):
        nonlocal pos
        return pos.distance_to(cluster_a.resource_cells[0].pos) - \
            pos.distance_to(cluster_b.resource_cells[0].pos)

    return sorted(sorted_clusters, key=cmp_to_key(compare))


def sort_clusters_by_centroid(
    pos: Position,
    clusters: List[Cluster]
) -> List[Cluster]:
    sorted_clusters = [cluster for _, cluster in clusters.items()
                       if len(cluster.resource_cells) > 0]

    def compare(cluster_a, cluster_b):
        nonlocal pos
        return pos.distance_to(cluster_a.get_centroid()) - \
            pos.distance_to(cluster_b.get_centroid())

    return sorted(sorted_clusters, key=cmp_to_key(compare))


def get_nearest_neighbor_cluster(cluster, clusters):
    distance = math.inf
    nearest = None

    for k in clusters:
        d = cluster.get_centroid().distance_to(
            clusters[k].get_centroid()
        )
        if d < distance:
            distance = d
            nearest = clusters[k]

    return nearest, distance

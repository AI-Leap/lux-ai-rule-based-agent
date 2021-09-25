def get_closest_cluster_by_centroid(citytile, clusters):
    closest_distance = 1000
    closest_cluster = None

    for key in clusters:
        distance = citytile.pos.distance_to(
            clusters[key].get_centroid()
        )
        if distance < closest_distance:
            closest_distance = distance
            closest_cluster = clusters[key]

    return closest_cluster, closest_distance

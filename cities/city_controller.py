from functools import cmp_to_key

import cities.city_service as CityService
import models.cluster_model as ClusterModel


def get_city_actions(
    game_state,
    game_state_info,
    player,
    clusters,
    player_id,
    opponent,
    opponent_id
):
    '''
    This is actually simple. We greedily build worker if possible.
    The only trick is if two citytiles can build only one worker,
    we decide which gets to build by calculating the score.
    '''
    actions = []
    units_capacity = sum([len(x.citytiles) for x in player.cities.values()])
    units_count = len(player.units)

    actionable_citytiles = []
    for city in player.cities.values():
        for citytile in city.citytiles:
            if citytile.can_act():
                actionable_citytiles.append(citytile)

    citytiles_to_be_sorted = []
    for citytile in actionable_citytiles:
        # We do not keep track of which cluster a citytile belongs to.
        # So, we need to find it here.
        closest_cluster, _ = CityService.get_closest_cluster_by_centroid(
            citytile,
            clusters
        )
        citytile_score = 0
        if closest_cluster is not None:
            citytile_score = ClusterModel.get_citytile_score(
                closest_cluster,
                game_state,
                player_id,
                opponent,
                opponent_id
            )

        citytiles_to_be_sorted.append({
            'citytile': citytile,
            'score': citytile_score
        })

    def compare(citytile1, citytile2):
        return citytile2['score'] - citytile1['score']

    sorted_citytiles = sorted(
        citytiles_to_be_sorted,
        key=cmp_to_key(compare)
    )

    for citytile in sorted_citytiles:
        if units_count < units_capacity and \
                game_state_info['turns_to_night'] > 4:
            actions.append(
                citytile['citytile'].build_worker()
            )
            units_count += 1
        else:
            if not player.researched_uranium():
                actions.append(
                    citytile['citytile'].research()
                )

    return actions

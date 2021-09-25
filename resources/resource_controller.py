import random
import resources.resource_service as ResourceService


def get_resources(game_state):
    return ResourceService.get_resources(game_state)


def find_closest_resource_tile(game_state, pos):
    resource_tiles = ResourceService.get_resources(game_state)
    closest_resource_tile, closest_distance = ResourceService \
        .get_closest_resource_tile(pos, resource_tiles)

    return closest_resource_tile, closest_distance


def get_random_resource(game_state):
    resource_tiles = ResourceService.get_resources(game_state)

    return random.choice(resource_tiles)

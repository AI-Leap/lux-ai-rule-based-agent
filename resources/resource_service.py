import math
from typing import List
from lux.game_map import Cell, Position, RESOURCE_TYPES


def get_resources(game_state) -> List[Cell]:
    '''
    Get all resource cells in the game map.
    '''
    resource_cells = []
    width, height = game_state.map_width, game_state.map_height
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_cells.append(cell)
    return resource_cells


def get_minable_resource_cells(
    player,
    resource_cells: List[Cell]
) -> List[Cell]:
    '''
    Get resource cells that can be mined by the player.
    '''
    minable_resource_types = [RESOURCE_TYPES.WOOD]
    if player.researched_coal():
        minable_resource_types.append(RESOURCE_TYPES.COAL)
    if player.researched_uranium():
        minable_resource_types.append(RESOURCE_TYPES.URANIUM)

    minable_resource_cells = [
        resource_cell for resource_cell in resource_cells
        if resource_cell.resource.type in minable_resource_types
    ]
    return minable_resource_cells


def get_closest_resource_tile(pos, resource_tiles):
    closest_distance = math.inf
    closest_resource_tile = None
    for resource_tile in resource_tiles:
        dist = resource_tile.pos.distance_to(pos)
        if dist < closest_distance:
            closest_distance = dist
            closest_resource_tile = resource_tile
    return closest_resource_tile, closest_distance


def get_resource_cells_by_positions(
    game_state,
    positions: List[Position]
) -> List[Cell]:
    '''
    Returns all the resource cells in given positions
    '''

    resource_cells = []

    for pos in positions:
        cell = game_state.map.get_cell_by_pos(pos)
        if cell.has_resource():
            resource_cells.append(cell)

    return resource_cells

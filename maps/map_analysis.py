import math
from typing import List
from collections import defaultdict
from functools import cmp_to_key
from lux.game_map import Cell, Position


def find_neighbors(v, resource_cells):
    '''
    This function returns the 8 neighbors if exist, of a given cell.
    We need to check if the neighbor is in resource cells because
    we want to return only neigbor resource cells.
    '''
    pos = v['pos']
    neighbors = []

    # N, S, E, W, NE, NW, SE, SW
    n = pos.translate('n', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(n)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    s = pos.translate('s', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(s)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    e = pos.translate('e', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(e)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    w = pos.translate('w', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(w)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    ne = n.translate('e', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(ne)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    nw = n.translate('w', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(nw)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    se = s.translate('e', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(se)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    sw = s.translate('w', 1)
    neighbor = next(
        (tile for tile in resource_cells if tile['pos'].equals(sw)),
        None
    )
    if neighbor is not None:
        neighbors.append(neighbor)

    return neighbors


def dfs(nodes, v):
    '''
    Standard Depth First Search implementation.
    We use iterative DFS because it is easier to debug and
    it is more suitable for this case.
    '''
    group = []

    stack = []
    stack.append(v)

    while len(stack):
        v = stack[-1]
        stack.pop()

        if not v['visited']:
            v['visited'] = True
            group.append(v)

        neighbors = find_neighbors(v, nodes)

        for neighbor in neighbors:
            if not neighbor['visited']:
                stack.append(neighbor)

    return group


def get_resource_groups(resource_cells: List[Cell]):
    '''
    Use Depth First Search to find connected components of resource cells.
    '''
    nodes = []
    for resource_cell in resource_cells:
        nodes.append({
            'pos': resource_cell.pos,
            'visited': False,
            'tile': resource_cell
        })

    groups = []
    for node in nodes:
        if not node['visited']:
            group = dfs(nodes, node)
            group = list(map(lambda x: x['tile'], group))
            groups.append(group)

    return groups


def get_perimeter(
    cells: List[Cell],
    width: int,
    height: int
) -> List[Position]:
    '''
    For all the given cells, this returns unique perimeter.
    Perimeter means 4 adjacent cells' positions. North, South, East, West.
    '''
    perimeter_dict = defaultdict()

    for tile in cells:
        n = tile.pos.translate('n', 1)
        s = tile.pos.translate('s', 1)
        e = tile.pos.translate('e', 1)
        w = tile.pos.translate('w', 1)

        sides = [n, s, e, w]

        for side in sides:
            side_tile = next(
                (t for t in cells if t.pos.equals(side)),
                None
            )

            if side_tile is None:
                if (side.x >= 0 and side.x < width) and \
                        (side.y >= 0 and side.y < height):
                    perimeter_dict[str(side.x) + str(side.y)] = side

    return list(perimeter_dict.values())


def get_full_perimeter(
    cells: List[Cell],
    width: int,
    height: int
) -> List[Position]:
    perimeter_dict = defaultdict()

    for tile in cells:
        n = tile.pos.translate('n', 1)
        s = tile.pos.translate('s', 1)
        e = tile.pos.translate('e', 1)
        w = tile.pos.translate('w', 1)
        ne = n.translate('e', 1)
        nw = n.translate('w', 1)
        se = s.translate('e', 1)
        sw = s.translate('w', 1)

        sides = [n, s, e, w, ne, nw, se, sw]

        for side in sides:
            side_tile = next(
                (t for t in cells if t.pos.equals(side)),
                None
            )

            if side_tile is None:
                if (side.x >= 0 and side.x < width) and \
                        (side.y >= 0 and side.y < height):
                    perimeter_dict[str(side.x) + str(side.y)] = side

    return list(perimeter_dict.values())


def sort_cells_by_distance(pos, cells: List[Cell]):
    def compare(cell1, cell2):
        nonlocal pos
        return pos.distance_to(cell1.pos) - pos.distance_to(cell2.pos)

    return sorted(cells, key=cmp_to_key(compare))


def get_closest_position(position, positions):
    closest_pos = None
    closest_distance = math.inf

    for pos in positions:
        distance = position.distance_to(pos)
        if distance < closest_distance:
            closest_distance = distance
            closest_pos = pos

    return closest_pos, closest_distance

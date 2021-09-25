from lux.game_map import Resource, Position
from clusters.cluster import Cluster


class Cell:
    def __init__(self, resource: Resource, x, y) -> None:
        self.resource = resource
        self.pos = Position(x, y)


def test_cluster():
    resource1 = Resource('wood', 4000)
    cell1 = Cell(resource1, 4, 3)

    resource2 = Resource('coal', 1000)
    cell2 = Cell(resource2, 5, 2)

    resource3 = Resource('uranium', 100)
    cell3 = Cell(resource3, 9, 2)

    cluster = Cluster('cluster_1', [cell1, cell2, cell3])

    assert cluster.resource_cells == [cell1, cell2, cell3]
    assert cluster.get_available_fuel() == 18000


def test_centroid():
    resource = Resource('uranium', 100)
    cell1 = Cell(resource, 2, 1)
    cell2 = Cell(resource, 2, 3)
    cell3 = Cell(resource, 3, 2)
    cell4 = Cell(resource, 3, 3)
    cell5 = Cell(resource, 4, 1)
    cell6 = Cell(resource, 4, 2)

    cluster = Cluster('cluster_2', [
        cell1,
        cell2,
        cell3,
        cell4,
        cell5,
        cell6,
    ])

    centroid = cluster.get_centroid()
    assert centroid.equals(Position(3, 2))


def test_centroid2():
    resource = Resource('uranium', 100)
    cluster = Cluster('cluster_3', [
        Cell(resource, 2, 4),
        Cell(resource, 3, 2),
        Cell(resource, 3, 4),
        Cell(resource, 3, 5),
        Cell(resource, 4, 4),
        Cell(resource, 4, 5),
        Cell(resource, 5, 3),
        Cell(resource, 5, 4),
        Cell(resource, 6, 4),
        Cell(resource, 6, 5),
        Cell(resource, 6, 6),
    ])

    centroid = cluster.get_centroid()
    assert centroid.equals(Position(4, 4))

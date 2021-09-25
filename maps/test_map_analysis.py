from lux.game_map import Cell, Position
import maps.map_analysis as MapAnalysis


def test_get_resource_groups():
    resource_cells = [
        Cell(13, 25),
        Cell(13, 26),
        Cell(14, 25),
        Cell(14, 26),
        Cell(12, 27),

        Cell(14, 21),
        Cell(14, 22),
        Cell(14, 23),
        Cell(15, 20)
    ]

    groups = MapAnalysis.get_resource_groups(resource_cells)
    assert len(groups) == 2

    assert isinstance(groups[0][0], Cell)
    assert isinstance(groups[1][0], Cell)
    assert len(groups[0]) == 5
    assert len(groups[1]) == 4


def test_get_resource_groups2():
    resource_tiles = [
        Cell(17, 0),
        Cell(18, 0),

        Cell(21, 2),
        Cell(22, 1),
        Cell(20, 3),
        Cell(20, 4),
        Cell(21, 4),

        Cell(15, 3),
        Cell(16, 4),
        Cell(17, 5),
        Cell(18, 5),
        Cell(17, 6),
        Cell(19, 6),
        Cell(16, 7),
    ]

    clusters = MapAnalysis.get_resource_groups(resource_tiles)
    assert len(clusters) == 3

    assert isinstance(clusters[0][0], Cell)
    assert isinstance(clusters[1][0], Cell)
    assert isinstance(clusters[2][0], Cell)

    assert len(clusters[0]) == 2
    assert len(clusters[1]) == 5
    assert len(clusters[2]) == 7


def test_get_resource_groups3():
    resource_tiles = [
        Cell(18, 0),
        Cell(17, 0),
        Cell(17, 1),

        Cell(21, 2),
        Cell(21, 3),

        Cell(15, 3),
        Cell(15, 4),
        Cell(15, 5),
    ]

    clusters = MapAnalysis.get_resource_groups(resource_tiles)
    assert len(clusters) == 3

    assert isinstance(clusters[0][0], Cell)
    assert isinstance(clusters[1][0], Cell)
    assert isinstance(clusters[2][0], Cell)

    assert len(clusters[0]) == 3
    assert len(clusters[1]) == 2
    assert len(clusters[2]) == 3


def test_get_resource_groups4():
    resource_cells = [
        Cell(2, 3),
        Cell(2, 4),
        Cell(2, 5),

        Cell(9, 3),
        Cell(9, 4),
        Cell(9, 5),

        Cell(5, 6),
        Cell(5, 7),
        Cell(6, 6),
        Cell(6, 7),
        Cell(4, 8),
        Cell(3, 9),
        Cell(7, 8),
        Cell(8, 9),
    ]

    groups = MapAnalysis.get_resource_groups(resource_cells)
    assert len(groups) == 3

    assert isinstance(groups[0][0], Cell)
    assert isinstance(groups[1][0], Cell)
    assert len(groups[0]) == 3
    assert len(groups[1]) == 3
    assert len(groups[2]) == 8


def test_get_perimeter():
    '''
        15  16  17  18  19
    4 | . | X | . | X | X |
    5 | X | X | X | X |
    6 | . | X |
    '''
    cluster = [
        Cell(15, 5),
        Cell(16, 5),
        Cell(17, 5),
        Cell(16, 4),
        Cell(16, 6),
        Cell(18, 5),
        Cell(18, 4),
        Cell(19, 4)
    ]

    perimeter = MapAnalysis.get_perimeter(cluster, width=20, height=7)
    assert len(perimeter) == 10
    assert isinstance(perimeter[0], Position)


def test_get_perimeter2():
    '''
        15  16  17  18  19
    4 | . | X | . | X | . |
    5 | . | X | . | X | . |
    '''
    cluster = [
        Cell(16, 4),
        Cell(16, 5),
        Cell(18, 4),
        Cell(18, 5),
    ]

    perimeter = MapAnalysis.get_perimeter(cluster, width=20, height=7)
    assert len(perimeter) == 10
    assert isinstance(perimeter[0], Position)


def test_get_perimeter3():
    cluster = [
        Cell(0, 6),
        Cell(0, 7)
    ]

    perimeter = MapAnalysis.get_perimeter(cluster, width=20, height=20)
    assert len(perimeter) == 4
    assert isinstance(perimeter[0], Position)


def test_get_perimeter4():
    cluster = [
        Cell(0, 19),
        Cell(0, 19)
    ]

    perimeter = MapAnalysis.get_perimeter(cluster, width=20, height=20)
    assert len(perimeter) == 2
    assert isinstance(perimeter[0], Position)


def test_sort_tile_by_distance():
    pos = Position(16, 8)
    cluster = [
        Cell(15, 5),
        Cell(16, 5),
        Cell(17, 4),
    ]
    sorted_cluster_tiles = MapAnalysis.sort_cells_by_distance(
        pos,
        cluster
    )

    assert sorted_cluster_tiles[0].pos.equals(Cell(16, 5).pos)
    assert sorted_cluster_tiles[1].pos.equals(Cell(15, 5).pos)
    assert sorted_cluster_tiles[2].pos.equals(Cell(17, 4).pos)

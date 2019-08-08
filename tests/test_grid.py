from layers.layer import Layer
from layers.mines import MinesLayer


def test_layer_choices():
    layer = Layer(height=3, width=3, default=0, choices={(1, 1): 5, (1, 2): 4})
    assert layer.raw_cells() == [[0, 0, 0], [0, 5, 4], [0, 0, 0]]


def test_layer_neighbors():
    """
      0 1 2
    0 . . .
    1 . n n
    2 . n x
  """
    n = set(Layer.each_neighbor(height=3, width=3, y=2, x=2))
    assert (1, 1) in n
    assert (1, 2) in n
    assert (2, 1) in n
    assert (2, 2) not in n
    assert (2, 3) not in n
    assert (3, 3) not in n
    assert (3, 2) not in n

    """
      0 1 2
    0 n n n
    1 n x n
    2 n n n
  """
    n2 = set(Layer.each_neighbor(height=3, width=3, y=1, x=1))
    assert (0, 0) in n2
    assert (0, 1) in n2
    assert (0, 2) in n2
    assert (1, 0) in n2
    assert (1, 1) not in n2
    assert (1, 2) in n2
    assert (2, 0) in n2
    assert (2, 1) in n2
    assert (2, 2) in n2


def test_layer_mines():
    fixture = [
        "x 1 . . . . . 1 1 1",
        "1 1 . . . . . 1 x 1",
        ". . 1 1 1 . . 1 1 1",
        ". . 1 x 2 1 . . . .",
        ". . 1 2 x 1 . . . .",
        ". . . 1 1 1 1 2 3 2",
        ". . . . . . 2 x x x",
        ". . . . . . 3 x 8 x",
        ". . . . . . 2 x x x",
        ". . . . . . 1 2 3 2",
    ]

    fixture_numbers = []

    for line in fixture:
        numbers = [
            -1 if x == "x" else 0 if x == "." else int(x) for x in line.split(" ")
        ]
        fixture_numbers.append(numbers)

    cell_lookups = {}

    for y in range(len(fixture_numbers)):
        for x in range(len(fixture_numbers[y])):
            cell_lookups[(y, x)] = fixture_numbers[y][x]

    mine_spots = {
        (0, 0),
        (1, 8),
        (3, 3),
        (4, 4),
        (6, 7),
        (6, 8),
        (6, 9),
        (7, 7),
        (7, 9),
        (8, 7),
        (8, 8),
        (8, 9),
    }

    layer = MinesLayer.with_mines_and_borders(
        height=10, width=10, mine_spots=mine_spots
    )
    raw_cells = layer.raw_cells()
    assert raw_cells == fixture_numbers

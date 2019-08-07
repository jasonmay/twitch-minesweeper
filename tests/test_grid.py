from grid import Layer

def test_layer_choices():
  layer = Layer(height=3, width=3, default=0, choices={(1, 1): 5, (1, 2): 4})
  assert layer.raw_cells() == [
    [0, 0, 0],
    [0, 5, 4],
    [0, 0, 0],
  ]

def test_layer_mines():
  layer = Layer(height=3, width=3, default=0, choices={(1, 1): 5, (1, 2): 4})
  assert layer.raw_cells() == [
    [0, 0, 0],
    [0, 5, 4],
    [0, 0, 0],
  ]

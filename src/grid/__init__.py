class Layer:

  def __init__(self, height, width, default, choices=None):
    """
    Examples:
    Layer(choices={(1, 1): 5, (1, 2): 4})
    Layer.from_lists([[5, 0, 0, 3]])
    """
    cells = []
    for row_index in range(height):
      row = []
      for column_index in range(width):
          row.append(
              choices.get((row_index, column_index), default)
            )

      cells.append(row)
    self.cells = cells

  @classmethod
  def with_mines_and_borders(Cls, height, width, mine_spots):
    cells = []
    for row_index in range(height):
      row = []
      for column_index in range(width):
          row.append(
              choices.get((row_index, column_index), default)
            )

      cells.append(row)
    self.cells = cells

  def raw_cells(self):
    return self.cells

class Grid:
  def __init__(self, mines_layer):
    self.mines_layer = mines_layer

  def check(self, y, x, flags):
    pass

  def _clear(self, y, x, flags):
    pass

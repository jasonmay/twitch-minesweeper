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

  def raw_cells(self):
    return self.cells

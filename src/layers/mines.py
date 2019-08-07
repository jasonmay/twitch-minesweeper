from layers.layer import Layer


class MinesLayer(Layer):

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


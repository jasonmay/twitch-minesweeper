class Layer:
    def __init__(self, height, width, default, choices=None):
        """
    Examples:
    Layer(height=3, width=3, choices={(1, 1): 5, (1, 2): 4})

    [[0, 0, 0],
     [0, 5, 4],
     [0, 0, 0]],

    Layer.from_lists([[5, 0, 0, 3]])
    """
        cells = []
        for row_index in range(height):
            row = []
            for column_index in range(width):
                if choices is not None:
                    row.append(choices.get((row_index, column_index), default))

            cells.append(row)
        self.cells = cells

    def raw_cells(self):
        return self.cells

    @classmethod
    def each_neighbor(Cls, y, x, height, width):
        for oy in [-1, 0, 1]:
            for ox in [-1, 0, 1]:
                if not oy and not ox:
                    continue

                ny = y + oy
                nx = x + ox

                if ny < 0 or ny >= height:
                    continue

                if nx < 0 or nx >= width:
                    continue

                yield (ny, nx)

    def cell_at(self, y, x):
        return self.cells[y][x]

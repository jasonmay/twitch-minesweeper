class Layer:
    def __init__(self, height, width, default, choices=None):
        # keep this thin since other subclasses will call this
        self._init_attrs(height, width, default, choices)

    @classmethod
    def with_cells(Cls, cells):
        height = len(cells)
        if height == 0:
            raise RuntimeError("Height must be more than 0")
        width = len(cells[0])
        if width == 0:
            raise RuntimeError("Width must be more than 0")

        layer = Cls(height=height, width=width, default=None)
        layer.cells = cells
        return layer

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

    def _init_attrs(self, height, width, default, choices=None):
        """
    Examples:
    Layer(height=3, width=3, choices={(1, 1): 5, (1, 2): 4})

    [[0, 0, 0],
     [0, 5, 4],
     [0, 0, 0]],

    Layer.with_cells([[5, 0, 0, 3]])
    """
        cells = []
        for row_index in range(height):
            row = []
            for column_index in range(width):
                if choices is not None:
                    value = choices.get((row_index, column_index), default)
                else:
                    value = default
                row.append(value)

            cells.append(row)
        self.cells = cells
        self.width = width
        self.height = height

    def raw_cells(self):
        return self.cells

    def cell_at(self, y, x):
        return self.cells[y][x]

    def set_cell(self, y, x, v):
        self.cells[y][x] = v

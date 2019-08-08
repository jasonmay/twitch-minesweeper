from layers.layer import Layer
import logging

logger = logging.getLogger("minesweeper")


# -1 = cleared, 0 = uncleared, 1 = flagged
"""
    def _clear(self, ph, pv):
        try:
            set the clear at pv, ph
        except IndexError as e:
            print(self.mask)
            print(str(e) + " ... {} x {}".format(ph, pv))
            raise

        if self.grid[pv][ph] > 0:
            # don't check anymore spots if we hit a spot that borders a mine
            return
        for nh, nv in self.neighbors(ph, pv):
            if self.mask[nv][nh] in [1, 2]:
                # already uncovered or is a flag
                continue
            self._clear(nh, nv)
"""


class CoverageLayer(Layer):
    def with_toggled_at(self, y, x):
        pass  # TODO

    def is_victory(self, mines_layer):
        uncleared_count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x] in [0, 1]:
                    uncleared_count += 1

        return uncleared_count == mines_layer.mines

    def with_checked_at(self, y, x, mines_layer):
        def _clear(y, x, height, width, cells, mines_layer):

            cells[y][x] = -1

            if mines_layer.cell_at(y, x) > 0:
                # don't check anymore spots if we hit a spot that borders a mine
                return
            for ny, nx in Layer.each_neighbor(y=y, x=x, width=width, height=height):
                if cells[ny][nx] in [-1, 1]:
                    continue
                _clear(ny, nx, height, width, cells, mines_layer)

        cells = self.cells
        if cells[y][x] != 0:
            # don't do anything if already cleared or is flagged
            return ("unchanged", None)

        if mines_layer.cell_at(y, x) == -1:
            return ("lost", None)

        _clear(y, x, self.height, self.width, cells, mines_layer)

        if self.is_victory(mines_layer):
            return ("won", None)

        return ("changed", self.__class__.with_cells(cells))

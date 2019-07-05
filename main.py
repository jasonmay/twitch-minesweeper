# beginner: 8x8, 10 mines
# intermediate: 16x16, 40 mines
# expert: 24x24, 99 mines

from random import sample
import re

mines = 40
size = (16, 16) # h, v


# State: Uncovered, Covered, Mine
# List[List[State]]


class Game:
    grid = []
    mask = []
    size = None
    mines = None
    pristine = True

    def neighbors(self, ph, pv, oob_cb=None):
        # all adjacent offsets of a mine
        offsets = [
            (-1, -1),
            (-1,  1),
            ( 1, -1),
            ( 1,  1),
            (-1,  0),
            ( 1,  0),
            ( 0, -1),
            ( 0,  1),
        ]
        for oh, ov in offsets:
            nh = ph + oh
            nv = pv + ov
            if not self.within_bounds(nh, nv):
                if callable(oob_cb):
                    oob_cb(self, nh, nv)
                continue
            yield (nh, nv)


    def _initialize_mines(self):
        h, v = self.size  # horizontal, vertical
        mine_choices_flat = sample(range(h * v), mines)
        mine_choices = {(x % h, x / v): True for x in mine_choices_flat}

        self.grid = []

        for iv in range(v):
            row = []
            for ih in range(h):
                row.append(-1 if mine_choices.get((ih, iv), False) else 0)
            self.grid.append(row)

        for ch, cv in mine_choices.keys():
            # all adjacent offsets of a mine
            for nh, nv in self.neighbors(ch, cv):
                if self.grid[nv][nh] == -1:
                    # neighboring piece is a mine
                    continue
                self.grid[nv][nh] += 1

    def __init__(self, mines, size):
        self.size = size
        self.mines = mines
        if mines >= size[0] * size[1]:
            raise ValueError("Invalid input: can't fit all the mines in the grid")

        h, v = size
        self.mask = []
        for iv in range(v):
            mask_row = []
            for ih in range(h):
                mask_row.append(0)
            self.mask.append(mask_row)

    def within_bounds(self, ph, pv):
        h, v = self.size
        if ph < 0 or ph >= h:
            return False
        if pv < 0 or pv >= v:
            return False
        return True

    def draw_unsolved(self):
        h, v = self.size
        print('  ' + ''.join([str(x % 10) for x in range(h)]))
        print('  ' + "-" * size[0])
        for iv in range(v):
            srow = "{} ".format(str(iv % 10))
            for ih in range(h):
                if self.mask[iv][ih] == 0:
                    srow += "."
                elif self.mask[iv][ih] == 2:
                    srow += "F"
                elif not self.pristine:
                    if self.grid[iv][ih] == 0:
                        srow += " "
                    elif self.grid[iv][ih] == -1:
                        srow += "X"
                    else:
                        srow += str(self.grid[iv][ih])
                else:
                    srow += "."

            print(srow)

    def draw_solved(self):
        h, v = self.size
        print('  ' + ''.join([str(x % 10) for x in range(h)]))
        print('  ' + "-" * size[0])

        for iv in range(v):
            srow = "{} ".format(str(iv % 10))
            for ih in range(h):
                if self.grid[iv][ih] == -1:
                    srow += "X"
                elif self.grid[iv][ih] == 0:
                    srow += " "
                else:
                    srow += str(self.grid[iv][ih])
            print(srow)

            # print(str(iv % 10) + ' ' + ''.join([" " if self.grid[iv][ih] == 0 else "X" if self.grid[iv][ih] == -1 else str(self.grid[iv][ih]) for ih in range(h)]))

        print('  ' + "-" * size[0])

    def _clear(self, ph, pv, cleared=set()):
        try:
            self.mask[pv][ph] = 1
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
            self._clear(nh, nv, cleared)

    def check(self, ph, pv):
        """
        Returns tuple
        First: -1 for error, 0 for continue as usual, 1 for game is over
        Second: for 1 type, True for won, False for lost
        """
        if not self.within_bounds(ph, pv):
            return (-1, None)

        if self.mask[ph][pv] in [1, 2]:
            # trying to check on a flag makes no sense
            return (0, None)

        if self.pristine:
            # try different setups until the first hit is guaranteed to be safe
            print("initializing mines")
            while True:
                self._initialize_mines()
                if self.grid[pv][ph] != -1:
                    break
            self.pristine = False

        gval = self.grid[pv][ph]
        if gval == -1:
            return (1, False)
        else:
            self._clear(ph, pv)
            # TODO check to see if the game is won here
        return (0, None)

    def flag(self, ph, pv):
        if not self.within_bounds(ph, pv):
            return -1

        if self.mask[pv][ph] == 1:
            return 0

        if self.mask[pv][ph] == 2:
            self.mask[pv][ph] = 0
        if self.mask[pv][ph] == 0:
            self.mask[pv][ph] = 2

        return 1


game = Game(mines, size)
cmd_validation = re.compile('(flag|check)\s+(\d+)\s+(\d+)', re.I)
while True:
    game.draw_unsolved()
    match_result = None
    while not match_result:
        print("Available commands:\nflag [column] [row]'\n'check [column] [row]'\n(example: check 0 12)")
        cmd = raw_input("> ").strip()
        match_result = cmd_validation.match(cmd)
        if not match_result:
            print("Invalid command!")

    cmd_type, scolumn, srow = match_result.groups()
    column, row = int(scolumn), int(srow)
    if cmd_type == "check":
        result, rtype = game.check(column, row)
        if result == 1:
            game.draw_unsolved()  # show the final result before bailing
            if rtype:
                print("you won")
            else:
                print("you lost")
            break
    elif cmd_type == "flag":
        game.flag(column, row)
    else:
        print("?????")

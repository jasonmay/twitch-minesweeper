from random import sample
class MineContext:
  def __init__(self, height, width):
    self.height = height
    self.width = width

  def generate_mines(self, mines, start_y, start_x):
    if mines >= self.height * self.width:
      raise RuntimeError("Too many mines for a ({}, {}) grid size. Game is unsolvable".format(self.height, self.width))

    all_coords = set((y, x) for y in range(self.height) for x in range(self.width)) - set((start_y, start_x))
    sample_coords = set(sample(all_coords, mines))

    return sample_coords

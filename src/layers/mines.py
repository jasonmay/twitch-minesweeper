from layers.layer import Layer


class MinesLayer(Layer):
  @classmethod
  def with_mines_and_borders(Cls, height, width, mine_spots):
    choices = {x: -1 for x in mine_spots}
    layer = Cls(height=height, width=width, default=0, choices=choices)

    print("\n".join(str(x) for x in layer.cells))
    for y, x in mine_spots:
      for ny, nx in Cls.each_neighbor(height=height, width=width, y=y, x=x):
        if (ny, nx) in mine_spots:
          continue

        layer.cells[ny][nx] += 1

    return layer

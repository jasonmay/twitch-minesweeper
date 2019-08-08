from commands import Command
from layers.mines import MinesLayer


class CheckCommand(Command):
    key_commands = " "

    def run(self, redraw_context):
        if self.interface_context.mines_layer is None:
            redraw_context.must_redraw_grid = True
            redraw_context.must_redraw_cursor = True
            mine_spots = self.interface_context.mine_context.generate_mines(
                self.interface_context.mines,
                self.interface_context.ycursor,
                self.interface_context.xcursor,
            )

            mines_layer = MinesLayer.with_mines_and_borders(
                height=self.interface_context.size[0],
                width=self.interface_context.size[1],
                mine_spots=mine_spots,
            )

            self.interface_context.mines_layer = mines_layer

        # TODO: actually propogate clearing here

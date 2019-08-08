from commands import Command
from layers.mines import MinesLayer


class FlagCommand(Command):
    key_commands = "f"

    def toggle_flag(self, y, x):
        cell = self.interface_context.coverage_layer.cell_at(y, x)
        if cell == 0:
            new_cell_value = 1
        elif cell == 1:
            new_cell_value = 0
        else:
            new_cell_value = None

        if new_cell_value is not None:
            self.interface_context.coverage_layer.set_cell(y, x, new_cell_value)

    def run(self, redraw_context):
        self.toggle_flag(self.interface_context.ycursor, self.interface_context.xcursor)
        redraw_context.must_redraw_grid = True

from importlib import import_module
import commands
from pathlib import Path
import inspect
import os
import re

from contexts.redraw import RedrawContext
from contexts.mines import MineContext


class Interface:
    ycursor = 0
    xcursor = 0

    def __init__(self, screen, h, w, mines):
        self.screen = screen
        self.size = (h, w)

        self.command_registry = self._build_command_registry()
        command_dispatch = {}

        self.mines = mines
        self.mines_layer = None
        self.mine_context = MineContext(height=h, width=w)

        for command_class in self.command_registry:
            command_instance = command_class(self)
            key_commands_raw = command_instance.key_commands
            if type(key_commands_raw) is not list:
                key_commands_raw = [key_commands_raw]

            key_commands = []
            for key_command in key_commands_raw:
                if type(key_command) is str:
                    key_commands.append(ord(key_command))
                elif type(key_comand) is int:
                    key_commands.append(key_command)
                else:
                    raise ValueError(
                        "Key command format '{}' not supported".format(str(key_command))
                    )

            for key_command in key_commands:
                command_dispatch[key_command] = command_instance

        self.command_dispatch = command_dispatch

    def _build_command_registry(self):
        registry = []
        for p_filename in Path('src/commands').glob('**/*.py'):
            filename = str(p_filename)
            if not os.path.isfile(filename):
                continue

            filename_parts = filename.split("/")

            # TODO find a better approach for python paths
            if filename_parts[0] == "src":
              filename_parts.pop(0)

            filename_parts[-1] = re.sub(r"\.py$", "", filename_parts[-1])
            module_str = ".".join(filename_parts)
            mod = import_module(module_str)
            for mod_variable_str in dir(mod):
                mod_variable = getattr(mod, mod_variable_str)
                if not inspect.isclass(mod_variable):
                    continue
                if mod_variable == commands.Command:
                    continue
                if not issubclass(mod_variable, commands.Command):
                    continue
                registry.append(mod_variable)

        return registry

    def within_bounds(self, y, x):
        if y < 0 or y >= self.size[0]:
            return False
        if x < 0 or x >= self.size[1]:
            return False
        return True

    def move(self, y, x, times=1):
        count = 0
        new_y = self.ycursor
        new_x = self.xcursor
        while count < times:
            new_y += y
            new_x += x

            if not self.within_bounds(new_y, new_x):
                break

            self.ycursor = new_y
            self.xcursor = new_x

            count += 1

        if new_y != self.ycursor or new_x != self.xcursor:
            self.must_redraw_cursor = True


    def move_left(self, spaces=1):
        self.move(0, -1, spaces)

    def move_right(self, spaces=1):
        self.move(0, 1, spaces)

    def move_up(self, spaces=1):
        self.move(-1, 0, spaces)

    def move_down(self, spaces=1):
        self.move(1, 0, spaces)

    def draw_grid(self):
        # TODO: (foo + 1) * 2 as a transform method?
        self.screen.addstr(0, 0, " " + "-" * ((self.size[1] + 1) * 2))
        for v in range(0, self.size[0]):
            line = "| "
            for h in range(0, self.size[1]):
              if self.mines_layer:
                cell =  self.mines_layer.cell_at(v, h)
                if cell > 0:
                  line += str(cell) + " "
                elif cell == 0:
                  line += ". "
                elif cell == -1:
                  line += "x "
                else:
                  line += "? "
              else:
                line += ". "
            line += "|"
            self.screen.addstr(v + 1, 0, line)

        self.screen.addstr(self.size[0] + 1, 0, " " + "-" * ((self.size[1] + 1) * 2))

    def run(self):
        self.screen.nodelay(1)
        last_key_input = None
        redraw_context = None
        while True:
            if last_key_input != -1:
                if not redraw_context or redraw_context.must_redraw_grid:
                    self.screen.clear()
                    self.draw_grid()
                if not redraw_context or redraw_context.must_redraw_cursor:
                    self.screen.move(self.ycursor + 1, (self.xcursor + 1) * 2)

            key_input = self.screen.getch()
            last_key_input = key_input

            # h j k l  y u b n  are directions
            if key_input in self.command_dispatch:
                redraw_context = RedrawContext()
                result = self.command_dispatch[key_input].run(redraw_context)
                self.screen.refresh()
                if result and result[0] == "quit":
                    break



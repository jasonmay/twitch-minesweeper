import curses
import time
import commands

import os
import inspect
import re
from importlib import import_module
from pathlib import Path

size = (25, 16)  # v, h


class RedrawContext:
    must_redraw_grid = False
    must_redraw_cursor = False


class Interface:
    ycursor = 0
    xcursor = 0

    def __init__(self, screen):
        self.screen = screen

        self.command_registry = self._build_command_registry()
        command_dispatch = {}

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
        for p_filename in Path('commands').glob('**/*.py'):
            filename = str(p_filename)
            if not os.path.isfile(filename):
                continue

            filename_parts = filename.split("/")
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


    def move_left(self, spaces=1):
        for space in range(spaces):
            if self.xcursor > 0:
                self.xcursor -= 1

        self.must_redraw_cursor = True

    def move_right(self, spaces=1):
        for space in range(spaces):
            if self.xcursor < size[1] - 1:
                self.xcursor += 1

    def move_up(self, spaces=1):
        for space in range(spaces):
            if self.ycursor > 0:
                self.ycursor -= 1

    def move_down(self, spaces=1):
        for space in range(spaces):
            if self.ycursor < size[0] - 1:
                self.ycursor += 1

    def draw_grid(self):
        # TODO: (foo + 1) * 2 as a transform method?
        self.screen.addstr(0, 0, " " + "-" * ((size[1] + 1) * 2))
        for v in range(0, size[0]):
            line = "| "
            for h in range(0, size[1]):
                line += ". "
                # TODO
            line += "|"
            self.screen.addstr(v + 1, 0, line)

        self.screen.addstr(size[0] + 1, 0, " " + "-" * ((size[1] + 1) * 2))

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
                # self.screen.addstr(30, 0, str(key_input))
                self.screen.refresh()
                if result and result[0] == "quit":
                    break
                # time.sleep(0.1)


def main(screen):
    interface = Interface(screen)
    interface.run()


if __name__ == "__main__":
    curses.wrapper(main)

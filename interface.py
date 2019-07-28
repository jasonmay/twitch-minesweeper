import curses
import time

size = (25, 16)  # v, h


class Command:
    def __init__(self, interface_context):
        self.interface_context = interface_context

    @property
    def key_commands(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class MoveLeftCommand(Command):
    key_commands = "h"

    def run(self):
        self.interface_context.move_left()


class MoveDownCommand(Command):
    key_commands = "j"

    def run(self):
        self.interface_context.move_down()


class MoveUpCommand(Command):
    key_commands = "k"

    def run(self):
        self.interface_context.move_up()


class MoveRightCommand(Command):
    key_commands = "l"

    def run(self):
        self.interface_context.move_right()


class QuitCommand(Command):
    key_commands = "q"

    def run(self):
        return ("quit", None)


class Interface:
    ycursor = 0
    xcursor = 0

    command_registry = [
        MoveUpCommand,
        MoveDownCommand,
        MoveRightCommand,
        MoveLeftCommand,
        QuitCommand,
    ]

    def __init__(self, stdscr):
        self.stdscr = stdscr

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

    def move_left(self, spaces=1):
        for space in range(spaces):
            if self.xcursor > 0:
                self.xcursor -= 1

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

    def run(self):
        # Clear screen

        while True:
            self.stdscr.clear()

            # TODO: (foo + 1) * 2 as a transform method?
            self.stdscr.addstr(0, 0, " " + "-" * ((size[1] + 1) * 2))
            for v in range(0, size[0]):
                line = "| "
                for h in range(0, size[1]):
                    line += ". "
                    # TODO
                line += "|"
                self.stdscr.addstr(v + 1, 0, line)

            self.stdscr.addstr(size[0] + 1, 0, " " + "-" * ((size[1] + 1) * 2))
            self.stdscr.move(self.ycursor + 1, (self.xcursor + 1) * 2)

            key_input = self.stdscr.getch()
            # h j k l  y u b n  are directions
            if key_input in self.command_dispatch:
                result = self.command_dispatch[key_input].run()
                # self.stdscr.addstr(30, 0, str(result))
                self.stdscr.refresh()
                # time.sleep(1)
                if result and result[0] == "quit":
                    break


def main(stdscr):
    interface = Interface(stdscr)
    interface.run()


if __name__ == "__main__":
    curses.wrapper(main)

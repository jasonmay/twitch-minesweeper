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

    def run(self, redraw_context):
        self.interface_context.move_left()
        redraw_context.must_redraw_cursor = True


class MoveDownCommand(Command):
    key_commands = "j"

    def run(self, redraw_context):
        self.interface_context.move_down()
        redraw_context.must_redraw_cursor = True


class MoveUpCommand(Command):
    key_commands = "k"

    def run(self, redraw_context):
        self.interface_context.move_up()
        redraw_context.must_redraw_cursor = True


class MoveRightCommand(Command):
    key_commands = "l"

    def run(self, redraw_context):
        self.interface_context.move_right()
        redraw_context.must_redraw_cursor = True


class QuitCommand(Command):
    key_commands = "q"

    def run(self, redraw_context):
        return ("quit", None)



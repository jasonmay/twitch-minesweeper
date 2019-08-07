from commands import Command


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


class MoveUpLeftCommand(Command):
    key_commands = "y"

    def run(self, redraw_context):
        self.interface_context.move(-1, -1)
        redraw_context.must_redraw_cursor = True


class MoveUpRightCommand(Command):
    key_commands = "u"

    def run(self, redraw_context):
        self.interface_context.move(-1, 1)
        redraw_context.must_redraw_cursor = True


class MoveDownLeftCommand(Command):
    key_commands = "b"

    def run(self, redraw_context):
        self.interface_context.move(1, -1)
        redraw_context.must_redraw_cursor = True


class MoveDownRightCommand(Command):
    key_commands = "n"

    def run(self, redraw_context):
        self.interface_context.move(1, 1)
        redraw_context.must_redraw_cursor = True

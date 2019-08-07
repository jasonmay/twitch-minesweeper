from commands import Command


class MoveLeftCommand(Command):
    key_commands = "H"

    def run(self, redraw_context):
        self.interface_context.move_left(5)
        redraw_context.must_redraw_cursor = True


class MoveDownCommand(Command):
    key_commands = "J"

    def run(self, redraw_context):
        self.interface_context.move_down(5)
        redraw_context.must_redraw_cursor = True


class MoveUpCommand(Command):
    key_commands = "K"

    def run(self, redraw_context):
        self.interface_context.move_up(5)
        redraw_context.must_redraw_cursor = True


class MoveRightCommand(Command):
    key_commands = "L"

    def run(self, redraw_context):
        self.interface_context.move_right(5)
        redraw_context.must_redraw_cursor = True


class MoveUpLeftCommand(Command):
    key_commands = "Y"

    def run(self, redraw_context):
        self.interface_context.move(-1, -1, 5)
        redraw_context.must_redraw_cursor = True


class MoveUpRightCommand(Command):
    key_commands = "U"

    def run(self, redraw_context):
        self.interface_context.move(-1, 1, 5)
        redraw_context.must_redraw_cursor = True


class MoveDownLeftCommand(Command):
    key_commands = "B"

    def run(self, redraw_context):
        self.interface_context.move(1, -1, 5)
        redraw_context.must_redraw_cursor = True


class MoveDownRightCommand(Command):
    key_commands = "N"

    def run(self, redraw_context):
        self.interface_context.move(1, 1, 5)
        redraw_context.must_redraw_cursor = True

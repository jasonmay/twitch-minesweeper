from commands import Command


class QuitCommand(Command):
    key_commands = "q"

    def run(self, redraw_context):
        return ("quit", None)

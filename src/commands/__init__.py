class Command:
    def __init__(self, interface_context):
        self.interface_context = interface_context

    @property
    def key_commands(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

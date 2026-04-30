class ParameterError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ConfigFileError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

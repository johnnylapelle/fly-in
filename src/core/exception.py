class ConfigFileError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GraphError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PathfindingError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

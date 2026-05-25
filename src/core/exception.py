class ConfigFileError(Exception):
    """Raised when a map file contains a syntax or validation error."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GraphError(Exception):
    """Raised when the graph is in an invalid state, such as a missing start or end zone."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PathfindingError(Exception):
    """Raised when the pathfinder fails to find a valid path for a drone."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

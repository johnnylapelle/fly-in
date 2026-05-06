from .connection import Connection
from .zone import Zone


class Drone:
    def __init__(self, id: int):
        self._id: int = id
        self._position: Zone | Connection | None = None
        self._path: list[tuple[Zone, int] | None] = []
        self._is_arrived: bool = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def position(self) -> Zone | Connection | None:
        return self._position

    @position.setter
    def position(self, new_pos: Zone | Connection) -> None:
        self._position = new_pos

    @property
    def path(self) -> list[tuple[Zone, int] | None]:
        return self._path

    @path.setter
    def path(self, path: list[tuple[Zone, int] | None]) -> None:
        self._path = path

    @property
    def is_arrived(self) -> bool:
        return self._is_arrived

    @is_arrived.setter
    def is_arrived(self) -> None:
        self._is_arrived = True

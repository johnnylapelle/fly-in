from .zone import Zone
from .connection import Connection


class Drone:
    def __init__(self, id: int, start: Zone):
        self._id: int = id
        self._position: Zone | Connection = start
        self._path: list[Zone] = []
        self._is_arrived: bool = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def position(self) -> Zone | Connection:
        return self._position

    @position.setter
    def position(self, new_pos: Zone | Connection) -> None:
        self._position = new_pos

    @property
    def path(self) -> list[Zone]:
        return self._path

    @property
    def is_arrived(self) -> bool:
        return self._is_arrived

    @is_arrived.setter
    def is_arrived(self) -> None:
        self._is_arrived = True

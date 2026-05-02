from .zone import Zone
from.connection import Connection


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

    @property
    def path(self) -> list[Zone]:
        return self._path

    @property
    def is_arrived(self) -> bool:
        return self._is_arrived

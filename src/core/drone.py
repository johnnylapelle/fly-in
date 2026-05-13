from typing import Union

from .connection import Connection
from .zone import Zone

Node = Union[Zone | Connection]


class Drone:
    def __init__(self, id: int):
        self._id: int = id
        self._position: Node | None = None
        self._path: list[tuple[Node, int]] = []
        self._is_arrived: bool = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def position(self) -> Node | None:
        return self._position

    @position.setter
    def position(self, new_pos: Node) -> None:
        self._position = new_pos

    @property
    def path(self) -> list[tuple[Node, int]]:
        return self._path

    @path.setter
    def path(self, path: list[tuple[Node, int]]) -> None:
        self._path = path

    @property
    def is_arrived(self) -> bool:
        return self._is_arrived

    @is_arrived.setter
    def is_arrived(self, x: bool) -> None:
        self._is_arrived = x

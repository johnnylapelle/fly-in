from typing import Union

from .connection import Connection
from .zone import Zone

Node = Union[Zone | Connection]


class Drone:
    """
    Represents a drone navigating through the graph.

    Holds the drone's current position, its full computed path
    (including connection transit states), and its simulation path
    (filtered for animation use).
    """

    def __init__(self, id: int):
        """
        Args:
            id: Unique identifier for this drone, used in logs and display.
        """

        self._id: int = id
        self._position: Node | None = None
        self._path: list[tuple[Node, int]] = []
        self._sim_path: list[tuple[Node, int]] = []
        self._is_arrived: bool = False

    @property
    def id(self) -> int:
        """Unique identifier for this drone."""

        return self._id

    @property
    def position(self) -> Node | None:
        """Current position of the drone, either a Zone or a Connection."""

        return self._position

    @position.setter
    def position(self, new_pos: Node) -> None:
        self._position = new_pos

    @property
    def path(self) -> list[tuple[Node, int]]:
        """Current position of the drone, either a Zone or a Connection."""

        return self._path

    @path.setter
    def path(self, path: list[tuple[Node, int]]) -> None:
        self._path = path

    @property
    def sim_path(self) -> list[tuple[Node, int]]:
        """
        Filtered path used by the simulator for animation.

        Contains only zones and restricted connection states,
        excluding normal connection transit states.
        """

        return self._sim_path

    @sim_path.setter
    def sim_path(self, path: list[tuple[Node, int]]) -> None:
        self._sim_path = path

    @property
    def is_arrived(self) -> bool:
        """True if the drone has reached the destination zone."""

        return self._is_arrived

    @is_arrived.setter
    def is_arrived(self, x: bool) -> None:
        self._is_arrived = x

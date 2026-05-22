from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsScene

from ..core.drone import Drone
from ..core.graph import Graph
from .connection_item import ConnectionItem
from .drone_item import DroneItem
from .zone_item import ZoneItem


class GraphScene(QGraphicsScene):
    """
    Qt scene that renders the graph and all its entities.

    Populates itself on construction with ConnectionItem, ZoneItem, and
    DroneItem instances for every connection, zone, and drone in the graph.
    """

    def __init__(self, graph: Graph, drones: list[Drone]):
        """
        Args:
            graph: The graph whose zones and connections are rendered.
            drones: The list of drones to render in the scene.
        """

        super().__init__()

        self.graph = graph
        self.drones = drones
        self._zones_items: list[ZoneItem] = []
        self._connections_items: list[ConnectionItem] = []
        self._drones_items: list[DroneItem] = []
        self._desc_visible: bool = True

        self.setBackgroundBrush(QBrush(QColor("#cbe2fe")))

        for connection in self.graph.connections.values():
            co_item = ConnectionItem(connection)
            self._connections_items.append(co_item)
            self.addItem(co_item)

        for zone in self.graph.zones.values():
            zone_item = ZoneItem(zone, self._on_zone_clicked)
            self._zones_items.append(zone_item)
            self.addItem(zone_item)

        for drone in self.drones:
            drone_item = DroneItem(drone)
            self._drones_items.append(drone_item)
            self.addItem(drone_item)

    @property
    def drones_items(self) -> list[DroneItem]:
        """Graphical items for each drone, in the same order as the drone list."""

        return self._drones_items

    def toggle_description(self) -> None:
        """Toggles the visibility of descriptions on all zone items."""

        self._desc_visible = not self._desc_visible
        for zone in self._zones_items:
            zone.set_description(self._desc_visible)

    def _on_zone_clicked(self, item: ZoneItem) -> None:
        """
        Callback triggered when a zone item is clicked.

        Args:
            item: The ZoneItem that was clicked.
        """

        item.toggle_desc()

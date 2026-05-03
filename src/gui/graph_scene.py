from PyQt6.QtWidgets import QGraphicsScene

from ..graph import Graph
from .connection_item import ConnectionItem
from .zone_item import ZoneItem


class GraphScene(QGraphicsScene):
    def __init__(self, graph: Graph):
        super().__init__()

        self.graph = graph
        self._zones: list[ZoneItem] = []
        self.connections: list[ConnectionItem] = []
        self._labels_visible: bool = True

        for connection in self.graph.connections.values():
            item = ConnectionItem(connection)
            self.connections.append(item)
            self.addItem(item)

        for zone in self.graph.zones.values():
            item = ZoneItem(zone, self._on_zone_clicked)
            self._zones.append(item)
            self.addItem(item)

    def toggle_labels(self) -> None:
        self._labels_visible = not self._labels_visible
        for zone in self._zones:
            zone.set_label_visible(self._labels_visible)

    def _on_zone_clicked(self, item: ZoneItem) -> None:
        item.toggle_label()

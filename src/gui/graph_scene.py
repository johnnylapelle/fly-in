from PyQt6.QtWidgets import QGraphicsScene

from ..graph import Graph
from .connection_item import ConnectionItem
from .zone_item import ZoneItem


class GraphScene(QGraphicsScene):
    def __init__(self, graph: Graph):
        super().__init__()

        self.graph = graph
        self.zones: list[ZoneItem] = []
        self.connections: list[ConnectionItem] = []

        for connection in self.graph.connections.values():
            item = ConnectionItem(connection)
            self.connections.append(item)
            self.addItem(item)

        for zone in self.graph.zones.values():
            print(zone)
            item = ZoneItem(zone)
            self.zones.append(item)
            self.addItem(item)

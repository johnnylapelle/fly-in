from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem

from ..connection import Connection
from .utils import SCALE


class ConnectionItem(QGraphicsLineItem):
    def __init__(self, connection: Connection):
        super().__init__()

        pen = self.init_pen()
        self.co = connection
        self.setLine(
            self.co.zone_a.x * SCALE,
            self.co.zone_a.y * SCALE,
            self.co.zone_b.x * SCALE,
            self.co.zone_b.y * SCALE
        )

        self.setPen(pen)

    def init_pen(self) -> QPen:
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("grey"))
        pen.setStyle(Qt.PenStyle.DashLine)

        return pen


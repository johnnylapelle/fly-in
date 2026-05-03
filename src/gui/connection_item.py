from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem

from ..connection import Connection
from .utils import SCALE


class ConnectionItem(QGraphicsLineItem):
    def __init__(self, connection: Connection):
        super().__init__()

        self.co = connection
        self.setLine(
            self.co.zone_a.x * SCALE,
            self.co.zone_a.y * SCALE,
            self.co.zone_b.x * SCALE,
            self.co.zone_b.y * SCALE
        )

        self.setPen(QPen(QColor("blue")))

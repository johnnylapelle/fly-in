# from PyQt6.QtCore import Qt
import random

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QGraphicsObject

from ..core.connection import Connection
from ..core.drone import Drone
from ..core.zone import Zone
from .utils import SCALE

from typing import Any


class DroneItem(QGraphicsObject):
    def __init__(self, drone: Drone) -> None:
        super().__init__()
        self.drone = drone

        self.pixmap = QPixmap("pngegg100.png")
        self.rect = QRectF(self.pixmap.rect())

        if isinstance(self.drone.position, Zone):
            zone = self.drone.position
            self.setPos(
                zone.x * SCALE,
                zone.y * SCALE)

        self.setRotation(random.randint(0, 360))

    def boundingRect(self) -> QRectF:
        return QRectF(
            -self.rect.width() / 2,
            -self.rect.height() / 2,
            self.rect.width(),
            self.rect.height()
        )

    def paint(self,
              painter: QPainter | None,
              option: Any, widget: Any = None) -> None:

        if isinstance(painter, QPainter):
            painter.drawPixmap(
                int(-self.rect.width() / 2),
                int(-self.rect.height() / 2),
                self.pixmap
            )

    def move(self) -> None:
        if isinstance(self.drone.position, Zone):
            zone = self.drone.position

            self.setPos(
                zone.x * SCALE,
                zone.y * SCALE)

        elif isinstance(self.drone.position, Connection):
            co = self.drone.position
            zone_a = co.zone_a
            zone_b = co.zone_b

            x = zone_a.x + zone_b.x / 2
            y = zone_a.y + zone_b.y / 2

            self.setPos(
                x * SCALE,
                y * SCALE)

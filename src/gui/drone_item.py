# from PyQt6.QtCore import Qt
import random
from typing import Any

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QGraphicsObject

from ..core.connection import Connection
from ..core.drone import Drone
from ..core.zone import Zone
from .utils import SCALE, get_fish


class DroneItem(QGraphicsObject):
    """
    Graphical representation of a drone in the scene.

    Renders as a fish pixmap centered on the drone's current position.
    Spawns with a random rotation. Supports both zone and connection
    positions for animation midpoints.
    """

    def __init__(self, drone: Drone) -> None:
        """
        Args:
            drone: The drone this item represents.
        """

        super().__init__()
        self.drone = drone

        self.pixmap = QPixmap(get_fish())
        self.rect = QRectF(self.pixmap.rect())

        if isinstance(self.drone.position, Zone):
            zone = self.drone.position
            self.setPos(
                zone.x * SCALE,
                zone.y * SCALE)

        self.setRotation(random.randint(0, 360))

    def boundingRect(self) -> QRectF:
        """Returns the bounding rectangle centered on the item's origin."""

        return QRectF(
            -self.rect.width() / 2,
            -self.rect.height() / 2,
            self.rect.width(),
            self.rect.height()
        )

    def paint(self,
              painter: QPainter | None,
              option: Any, widget: Any = None) -> None:
        """Draws the fish pixmap centered on the item's origin."""

        if isinstance(painter, QPainter):
            painter.drawPixmap(
                int(-self.rect.width() / 2),
                int(-self.rect.height() / 2),
                self.pixmap
            )

    def move(self) -> None:
        """
        Moves the item to the drone's current position.

        Handles both Zone and Connection positions. For connections,
        the item is placed at the midpoint between the two connected zones.
        """

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

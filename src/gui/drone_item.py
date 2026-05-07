from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem

from ..core.drone import Drone
# from ..core.connection import Connection
# from .utils import SCALE


class DroneItem(QGraphicsPixmapItem):
    def __init__(self, drone: Drone) -> None:
        super().__init__()
        self.drone = drone

        pixmap = QPixmap("pngegg100.png")
        self.setPixmap(pixmap)
        rect = self.boundingRect()

        # if isinstance(self.drone.position, Drone):
        #     self.setPos(
        #         self.drone.position.x * SCALE,
        #         self.drone.position.y * SCALE)

        self.setPos(
            -rect.width() / 2,
            -rect.height() / 2)

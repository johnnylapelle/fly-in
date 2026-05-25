from typing import Callable

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import (QGraphicsEllipseItem, QGraphicsSceneMouseEvent,
                             QGraphicsTextItem)

from ..core.zone import Zone
from .utils import RADIUS, SCALE, get_color


class ZoneItem(QGraphicsEllipseItem):
    """
    Graphical representation of a zone in the scene.

    Renders as a colored circle with a description label showing the
    zone name, type, and drone capacity. Supports click-to-toggle
    description visibility. Zones with color 'rainbow' cycle through
    hues continuously via a QTimer.
    """

    def __init__(self,
                 zone: Zone, on_click: Callable[['ZoneItem'], None]) -> None:
        """
        Args:
            zone: The zone to render.
            on_click: Callback invoked when the item is clicked,
                receiving this ZoneItem as argument.
        """

        QGraphicsEllipseItem.__init__(
            self, -RADIUS / 2, -RADIUS / 2, RADIUS, RADIUS)

        self._zone = zone
        self.setPos(zone.x * SCALE, zone.y * SCALE)

        # color
        if zone.color == "rainbow":
            self.hue = 0
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_color)
            self.timer.start(30)
        else:
            pen = QPen(QColor(get_color(zone.color)))
            pen.setWidth(3)

            brush = QBrush(QColor(get_color(zone.color)))

            self.setPen(pen)
            self.setBrush(brush)

        # display zone informations
        self.desc = QGraphicsTextItem(self)
        self.desc.setTextWidth(200)
        self.desc.setHtml(
            f"<center>{self._zone.name}<br>"
            f"{self._zone.type}<br>"
            f"{self._zone.max_drones} drones</center>")
        rect = self.desc.boundingRect()
        self.desc.setPos(-rect.width() / 2, rect.height() / 2 + 25)
        self.desc.setDefaultTextColor(QColor("black"))

        self._on_click = on_click

    def toggle_desc(self) -> None:
        """Toggles the visibility of the description label."""

        self.desc.setVisible(not self.desc.isVisible())

    def set_description(self, on_off: bool) -> None:
        """
        Sets the description label visibility explicitly.

        Args:
            on_off: True to show, False to hide.
        """

        self.desc.setVisible(on_off)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        """Forwards the click event to the on_click callback."""

        self._on_click(self)
        return super().mousePressEvent(event)

    def update_color(self) -> None:
        """Advances the hue by 2 degrees for the rainbow color animation."""

        color = QColor.fromHsv(self.hue, 255, 255)

        self.setBrush(QBrush(color))
        self.setPen(QPen(color))

        self.hue = (self.hue + 2) % 360

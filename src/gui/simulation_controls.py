from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QPainter
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QStyle, QWidget

from ..simulation.simulation_state import SimulationState
from .utils import get_style


class SimControls(QWidget):
    prev_requested = pyqtSignal()
    play_requested = pyqtSignal()
    next_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._btn_prev = QPushButton()
        self._btn_play = QPushButton()
        self._btn_next = QPushButton()

        for btn in (self._btn_prev, self._btn_play, self._btn_next):
            layout.addWidget(btn)

        self._btn_prev.clicked.connect(self.prev_requested)
        self._btn_play.clicked.connect(self.play_requested)
        self._btn_next.clicked.connect(self.next_requested)

        self._set_icons()

    def _set_icons(self) -> None:
        style = get_style()
        white = QColor("white")

        self._btn_prev.setIcon(self._colorize_icon(
            style.standardIcon(
                QStyle.StandardPixmap.SP_MediaSkipBackward), white))

        self._btn_play.setIcon(self._colorize_icon(
            style.standardIcon(
                QStyle.StandardPixmap.SP_MediaPlay), white))

        self._btn_next.setIcon(self._colorize_icon(
            style.standardIcon(
                QStyle.StandardPixmap.SP_MediaSkipForward), white))

    def _colorize_icon(self, icon: QIcon, color: QColor) -> QIcon:
        pixmap = icon.pixmap(24, 24)
        painter = QPainter(pixmap)
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return QIcon(pixmap)

    def set_playing(self, state: SimulationState) -> None:
        if state == SimulationState.RUNNING:
            pixmap = (QStyle.StandardPixmap.SP_MediaPause)
        elif state == SimulationState.FINISHED:
            pixmap = (QStyle.StandardPixmap.SP_ArrowBack)
        else:
            pixmap = (QStyle.StandardPixmap.SP_MediaPlay)

        white = QColor("white")
        self._btn_play.setIcon(self._colorize_icon(
            get_style().standardIcon(pixmap), white))

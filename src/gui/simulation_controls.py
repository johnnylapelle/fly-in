from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QPainter
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QStyle, QWidget

from ..simulation.simulation_state import SimulationState
from .utils import get_style


class SimControls(QWidget):
    """
    Playback control bar with previous, play/pause, and next buttons.

    Displayed at the bottom center of the window. Emits signals on user
    interaction. The play button icon updates to reflect the current
    simulation state.

    Signals:
        prev_requested: Emitted when the user clicks the previous button.
        play_requested: Emitted when the user clicks the play/pause button.
        next_requested: Emitted when the user clicks the next button.
    """

    prev_requested = pyqtSignal()
    play_requested = pyqtSignal()
    next_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Args:
            parent: Parent widget. Pass the main window to render
                the controls as an overlay.
        """

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
        """Sets the initial white icons on all three buttons."""

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
        """
        Returns a recolored copy of the given icon.

        Preserves the icon's shape (alpha channel) and replaces its
        color using SourceIn composition mode.

        Args:
            icon: The icon to recolor.
            color: The target color.

        Returns:
            A new QIcon with the applied color.
        """

        pixmap = icon.pixmap(24, 24)
        painter = QPainter(pixmap)
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return QIcon(pixmap)

    def set_playing(self, state: SimulationState) -> None:
        """
        Returns a recolored copy of the given icon.

        Preserves the icon's shape (alpha channel) and replaces its
        color using SourceIn composition mode.

        Args:
            icon: The icon to recolor.
            color: The target color.

        Returns:
            A new QIcon with the applied color.
        """

        if state == SimulationState.RUNNING:
            pixmap = (QStyle.StandardPixmap.SP_MediaPause)
        elif state == SimulationState.FINISHED:
            pixmap = (QStyle.StandardPixmap.SP_ArrowBack)
        else:
            pixmap = (QStyle.StandardPixmap.SP_MediaPlay)

        white = QColor("white")
        self._btn_play.setIcon(self._colorize_icon(
            get_style().standardIcon(pixmap), white))

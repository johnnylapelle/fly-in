from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class OverlayPanel(QWidget):
    """
    Overlay panel with map and simulation controls.

    Displayed in the top-left corner of the window. Emits signals on
    user interaction rather than acting directly, keeping it decoupled
    from the rest of the application.

    Signals:
        load_map_requested: Emitted when the user clicks Load Map.
        toggle_desc_requested: Emitted when the user clicks Hide/Show Description.
        reset_requested: Emitted when the user clicks Reset.
    """

    load_map_requested = pyqtSignal()
    toggle_desc_requested = pyqtSignal()
    reset_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Args:
            parent: Parent widget. Pass the main window to render
                the panel as an overlay.
        """

        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._btn_load_map = QPushButton('Load Map (M)')
        self._btn_toggle_desc = QPushButton('Hide Description (H)')
        self._btn_reset = QPushButton('Reset (R)')

        for btn in (self._btn_load_map,
                    self._btn_toggle_desc,
                    self._btn_reset):
            layout.addWidget(btn)

        self._btn_load_map.clicked.connect(self.load_map_requested)
        self._btn_toggle_desc.clicked.connect(self.toggle_desc_requested)
        self._btn_reset.clicked.connect(self.reset_requested)

    def set_text_description(self, visible: bool) -> None:
        """
        Updates the description button label to reflect current visibility.

        Args:
            visible: If True, sets the label to 'Hide Description'.
                If False, sets it to 'Show Description'.
        """

        self._btn_toggle_desc.setText(
            'Hide Description (H)' if visible else 'Show Description (H)'
        )

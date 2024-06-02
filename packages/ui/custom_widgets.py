"""
This module contains custom widgets.
"""

from PySide6 import QtCore
from PySide6.QtWidgets import QLineEdit, QLabel


class CustomQLineEdit(QLineEdit):
    """
    A custom QLineEdit widget with a fixed size.

    This widget inherits from QLineEdit and sets a fixed size of 215x40 pixels.
    Each instance of this class is stored in the class-level `instances` dictionary,
    with the placeholder text as the key.
    """

    instances: dict = {}

    def __init__(self, parent=None, placeholder_text: str = None):
        super().__init__(parent=parent)

        self.setFixedSize(215, 40)

        if placeholder_text and isinstance(placeholder_text, str):
            self.setPlaceholderText(placeholder_text)
            CustomQLineEdit.instances[placeholder_text] = self


class CustomQLabel(QLabel):
    """A customized QLabel class for creating labels with specific styles and properties."""

    def __init__(self, parent=None, size: tuple[int, int] = None, text: str = None):
        super().__init__(parent=parent)

        if text:
            self.setText(text)

        if size:
            self.setFixedSize(*size)

        self.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        self.setStyleSheet("color: #000000; background: #87A9B5; border-radius: 15px;")

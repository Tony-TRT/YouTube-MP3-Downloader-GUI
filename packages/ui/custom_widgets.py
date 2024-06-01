"""
This module contains custom widgets.
"""

from PySide6.QtWidgets import QLineEdit


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

"""
This module provides utility functions for managing the appearance of the user interface.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap

from packages.constants import constants


class AestheticWindow(QWidget):

    def __init__(self):

        super().__init__()
        self.images: dict = {image_name: QPixmap(image_path) for image_name, image_path in constants.IMAGES.items()}

        if constants.STYLE.exists():
            self.ui_apply_style()

    def ui_apply_style(self) -> None:
        """Loads application style."""

        with open(constants.STYLE, "r", encoding="UTF-8") as style:
            self.setStyleSheet(style.read())

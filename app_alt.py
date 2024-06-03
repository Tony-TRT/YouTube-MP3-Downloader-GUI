"""
Main application file.
"""

import sys

from PySide6 import QtWidgets

from packages.ui.aesthetic import AestheticWindow
from packages.ui.custom_widgets import CustomQLineEdit, CustomQLabel, CustomQProgressBar


class MainWindow(AestheticWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube MP3 Downloader")
        self.setFixedSize(900, 500)

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = None

        self.ui_manage_layouts()

        ##################################################
        # Widgets.
        ##################################################

        self.label_background = None
        self.label_drop_info = None
        self.label_album_cover = None
        self.progress_bar = None
        self.le_youtube_url = None
        self.btn_download = None
        self.btn_settings = None

        self.ui_manage_widgets()

        ##################################################
        # Graphics.
        ##################################################

        self.ui_manage_graphics()

    def ui_manage_graphics(self) -> None:
        """Graphics are managed here."""

        self.setWindowIcon(self.images["logo"])
        self.label_background.setPixmap(self.images["background"])
        self.label_album_cover.setPixmap(self.images["drop_cover"])
        self.le_youtube_url.addAction(self.images["YouTube"], self.le_youtube_url.ActionPosition.LeadingPosition)

        for key, value in CustomQLineEdit.instances.items():
            value.addAction(self.images[key.lower().replace(" ", "_")], value.ActionPosition.LeadingPosition)

        self.btn_download.setIcon(self.images["download"])
        self.btn_settings.setIcon(self.images["settings"])

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here."""

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here."""

        self.label_background = QtWidgets.QLabel(self)
        self.label_drop_info = CustomQLabel(self.label_background, (360, 40), "Drop the album cover below.")
        self.label_album_cover = CustomQLabel(self.label_background, (360, 220))
        self.progress_bar = CustomQProgressBar(parent=self.label_background)
        self.le_youtube_url = QtWidgets.QLineEdit(self.label_background)
        self.le_youtube_url.setPlaceholderText("Paste YouTube link here.")
        self.le_youtube_url.setFixedSize(405, 40)

        placeholders: list[str] = [
            "Title", "Artist", "Album", "Year", "Genre", "Copyright",
            "Disc Number", "Total Discs", "Track Number", "Total Tracks"
        ]

        for placeholder in placeholders:
            CustomQLineEdit(parent=self.label_background, placeholder_text=placeholder)

        self.btn_download = QtWidgets.QPushButton(parent=self.label_background, text="Download")
        self.btn_download.setFixedSize(215, 95)
        self.btn_settings = QtWidgets.QPushButton(parent=self.label_background, text="Settings")
        self.btn_settings.setFixedSize(215, 95)

        self.main_layout.addWidget(self.label_background)

        self.label_drop_info.move(20, 170)
        self.label_album_cover.move(20, 220)
        self.le_youtube_url.move(20, 55)
        y_coordinate: int = 170

        for index, custom_line_edit in enumerate(CustomQLineEdit.instances.values()):
            x_coordinate: int = 455 if index % 2 == 0 else 680
            y_coordinate: int = y_coordinate + 50 if index in {2, 4, 6, 8} else y_coordinate
            custom_line_edit.move(x_coordinate, y_coordinate)

        self.btn_download.move(455, 65)
        self.btn_settings.move(680, 65)


if __name__ == '__main__':
    root = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    root.exec()

"""
Main application file.
"""

import sys

from PySide6 import QtWidgets

from packages.ui.aesthetic import AestheticWindow


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
        self.le_youtube_url = None
        self.le_album = None
        self.le_artist = None
        self.le_disc_number = None
        self.le_total_discs = None
        self.le_track_number = None
        self.le_total_tracks = None
        self.le_track_title = None
        self.le_year = None
        self.btn_download = None
        self.btn_settings = None

        self.ui_manage_widgets()

        ##################################################
        # Graphics.
        ##################################################

        self.ui_manage_graphics()

    def ui_manage_graphics(self) -> None:
        """Graphics are managed here."""

        self.setWindowIcon(self.images.get("logo"))
        self.label_background.setPixmap(self.images.get("background"))
        self.le_youtube_url.addAction(self.images.get("YouTube"), self.le_youtube_url.ActionPosition.LeadingPosition)
        self.btn_download.setIcon(self.images.get("download"))
        self.btn_settings.setIcon(self.images.get("settings"))

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here."""

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here."""

        self.label_background = QtWidgets.QLabel(self)
        self.le_youtube_url = QtWidgets.QLineEdit(self.label_background)
        self.le_youtube_url.setPlaceholderText("Paste YouTube link here.")
        self.le_youtube_url.setFixedSize(405, 40)
        self.btn_download = QtWidgets.QPushButton(parent=self.label_background, text="Download")
        self.btn_download.setFixedSize(215, 95)
        self.btn_settings = QtWidgets.QPushButton(parent=self.label_background, text="Settings")
        self.btn_settings.setFixedSize(215, 95)

        self.main_layout.addWidget(self.label_background)

        self.le_youtube_url.move(20, 55)
        self.btn_download.move(455, 65)
        self.btn_settings.move(680, 65)


if __name__ == '__main__':
    root = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    root.exec()

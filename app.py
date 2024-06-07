"""
Main application file.
"""

import sys
from functools import partial

from PySide6 import QtWidgets

from packages.logic import toolkit, bg_processes
from packages.ui.aesthetic import AestheticWindow
from packages.ui.custom_widgets import CustomQLineEdit, CustomQLabel, CustomQProgressBar


class MainWindow(AestheticWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube MP3 Downloader")
        self.setFixedSize(900, 500)
        self.setAcceptDrops(True)
        self.thread = bg_processes.DownloadAndProcess()
        self.current_cover = None
        self.placeholders: list[str] = [
            "Title",
            "Artist",
            "Album",
            "Year",
            "Genre",
            "Copyright",
            "Disc Number",
            "Total Discs",
            "Track Number",
            "Total Tracks"
        ]

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

        ##################################################
        # Connections.
        ##################################################

        self.logic_connect_widgets()

    def dragEnterEvent(self, event):

        event.accept()

    def dropEvent(self, event):
        """Handle file drop events, process image files, and update the album cover label."""

        event.accept()
        dropped_file = event.mimeData().urls()[0].toLocalFile()

        if dropped_file.split('.')[-1].casefold() in ['jpg', 'jpeg', 'png', 'bmp']:

            self.current_cover = toolkit.process_album_cover(image=dropped_file)
            self.label_album_cover.setPixmap(self.current_cover[0])

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

        for placeholder in self.placeholders:
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

    def logic_connect_widgets(self) -> None:
        """Connections are managed here."""

        self.btn_download.clicked.connect(self.logic_main_process)
        self.btn_settings.clicked.connect(self.logic_open_settings)
        self.thread.download_finished.connect(partial(self.logic_display_information, 1))
        self.thread.file_converted.connect(partial(self.logic_display_information, 2))
        self.thread.file_tagged.connect(partial(self.logic_display_information, 3))
        self.thread.error_happened.connect(partial(self.logic_display_information, -1))

    def logic_display_information(self, signal: int) -> None:
        """Displays information to the user regarding the progress or errors encountered.
        This information is shown in the window title and / or updated on the progress bar.

        Args:
            signal (int): The signal associated with the information to be communicated.
        """

        signal_map: dict = {
            -3: (" - One or more tags are non-numeric.", 0),
            -2: (" - The provided link is not a valid YouTube link.", 0),
            -1: (" - An error has occurred.", 0),
            0: (" - Downloading...", 0),
            1: (" - Converting...", 35),
            2: (" - Writing metadata...", 70),
            3: (" - Success!", 100)
        }

        self.setWindowTitle("YouTube MP3 Downloader" + signal_map[signal][0])
        self.progress_bar.setValue(signal_map[signal][1])

    def logic_main_process(self) -> None:
        """Processes the information entered by the user and attempts to create the desired mp3 file."""

        line_edits: dict = CustomQLineEdit.instances
        youtube_link: str = self.le_youtube_url.text()

        if not toolkit.check_link(text=youtube_link):
            self.logic_display_information(signal=-2)
            return

        requires_num_value: list = [le for key, le in line_edits.items() if key == "Year" or " " in key]
        strings: list[str] = [le.text() for le in requires_num_value]

        if not toolkit.check_data(strings=strings):
            self.logic_display_information(signal=-3)
            return

        tags: dict = {phr.lower().replace(" ", "_"): line_edits[phr].text() for phr in self.placeholders}
        tags["disc_number"] = f"{line_edits["Disc Number"].text()}/{line_edits["Total Discs"].text()}"
        tags["track_number"] = f"{line_edits["Track Number"].text()}/{line_edits["Total Tracks"].text()}"
        tags["cover"] = self.current_cover[1] if self.current_cover else None

        self.logic_display_information(signal=0)
        self.thread.set_url(link=youtube_link)
        self.thread.set_metadata(metadata=tags)
        self.thread.start()

    def logic_open_settings(self) -> None:

        ...


if __name__ == '__main__':
    root = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    root.exec()

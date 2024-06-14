"""
Main application file.
"""

import sys
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

from packages.logic import toolkit, bg_processes
from packages.ui.aesthetic import AestheticWindow
from packages.ui.custom_widgets import CustomQLineEdit, CustomQLabel, CustomQProgressBar


class MainWindow(AestheticWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube MP3 Downloader")
        self.setFixedSize(900, 500)
        self.setAcceptDrops(True)
        self.process_thread = bg_processes.DownloadAndProcess()
        self.legal_thread = bg_processes.DetectVideoCopyright()
        self.current_cover = None
        self.mp3_quality: str = "192k"
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
        self.le_youtube_url.textChanged.connect(self.logic_legal_information)
        self.process_thread.download_finished.connect(partial(self.logic_display_information, 1))
        self.process_thread.file_converted.connect(partial(self.logic_display_information, 2))
        self.process_thread.file_tagged.connect(partial(self.logic_display_information, 3))
        self.process_thread.error_happened.connect(partial(self.logic_display_information, -1))
        self.legal_thread.this_is_ok_signal.connect(partial(self.logic_show_legal_warning, False))
        self.legal_thread.this_is_not_ok_signal.connect(partial(self.logic_show_legal_warning, True))

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

    def logic_legal_information(self) -> None:
        """Initiates a legal information check process for the YouTube video URL entered."""

        if not toolkit.check_link(text=self.le_youtube_url.text()):
            return

        setattr(self.legal_thread, "youtube_url", self.le_youtube_url.text())
        self.legal_thread.start()

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
        setattr(self.process_thread, "youtube_link", youtube_link)
        setattr(self.process_thread, "metadata", tags)
        setattr(self.process_thread, "quality", self.mp3_quality)
        self.process_thread.start()

    def logic_open_settings(self) -> None:
        """Opens a dialog for selecting the mp3 audio quality."""

        # Setting up the QMessageBox
        win = QMessageBox(self)
        win.setIcon(QMessageBox.Question)  # type: ignore
        win.setWindowTitle("Settings")
        win.setText("Please select the audio quality for the mp3")
        win.setStyleSheet("QLabel {color: black} QPushButton {width: 120px; height: 40px}")

        # Creating the buttons
        options: list[str] = ["128", "192", "320"]
        buttons: dict = {
            win.addButton(opt + " kbps", QMessageBox.ActionRole): opt + "k" for opt in options  # type: ignore
        }
        win.exec()

        # Record the user's choice
        self.mp3_quality: str = buttons[win.clickedButton()]

    def logic_show_legal_warning(self, flag: bool) -> None:
        """Controls the display of a legal warning based on the given flag.

        Args:
            flag (bool): Indicates whether to display the legal warning or not.
        """


if __name__ == '__main__':
    root = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    root.exec()

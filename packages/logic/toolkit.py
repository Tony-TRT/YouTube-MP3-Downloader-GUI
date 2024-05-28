"""
This module contains useful tools for the application.
"""

from PIL import Image
from io import BytesIO
from PySide6.QtGui import QPixmap


def check_link(text: str) -> bool:
    """Check if a given text string contains a valid YouTube link.

    Args:
        text (str): The text string to check.

    Returns:
        bool: True if all conditions are met, indicating a valid YouTube link format; False otherwise.
    """

    step_01: bool = "www.youtube.com" in text
    step_02: bool = text.startswith("https://") or text.startswith("www.")
    step_03: bool = text.count(".") == 2

    return step_01 and step_02 and step_03


def check_data(strings: list[str]) -> bool:
    """Check if all strings in a list are composed only of digits or are empty.

    Args:
        strings (list[str]): A list of strings to check.

    Returns:
        bool: True if all strings in the list contain only digits or are empty; False otherwise.
    """

    return all(string.isdigit() or not string for string in strings)


def process_album_cover(image: str) -> tuple[QPixmap, bytes]:
    """Process an album cover image by removing metadata, resizing,
    and converting it to both QPixmap and binary data formats.

    Args:
        image (str): The file path to the album cover image.

    Returns:
        tuple[QPixmap, bytes]: A tuple containing:
            - QPixmap: The image as a QPixmap, suitable for display in a PySide6 application.
            - bytes: The image data in PNG format, suitable for tagging an MP3 file.
    """

    image: Image = Image.open(image)

    # Remove metadata by creating a new image with the same data
    data: list = list(image.getdata())
    new_image: Image = Image.new(image.mode, image.size)
    new_image.putdata(data)

    # Resize the image to 200x200 pixels
    new_image: Image = new_image.resize((200, 200))

    # Save the processed image to a byte array in PNG format
    byte_array: BytesIO = BytesIO()
    new_image.save(byte_array, format='PNG')
    byte_data: bytes = byte_array.getvalue()

    pixmap = QPixmap()
    pixmap.loadFromData(byte_data)
    return pixmap, byte_data

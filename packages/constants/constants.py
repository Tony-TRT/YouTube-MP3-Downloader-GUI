"""
This module contains all the constants used in the application.
These constants can be imported and used throughout the project to maintain
consistency and ease of updates.
"""

from typing import final
from pathlib import Path


BASE_FOLDER: final(Path) = Path(__file__).resolve().parent.parent.parent
RESOURCES_FOLDER: final(Path) = Path.joinpath(BASE_FOLDER, "resources")
IMAGES_FOLDER: final(Path) = Path.joinpath(RESOURCES_FOLDER, "images")
IMAGES: final(dict) = {image_path.stem: str(image_path) for image_path in IMAGES_FOLDER.iterdir()}
STYLE_FOLDER: final(Path) = Path.joinpath(RESOURCES_FOLDER, "style")
STYLE: final(Path) = Path.joinpath(STYLE_FOLDER, "style.qss")

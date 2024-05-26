"""
This module contains useful tools for the application.
"""


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
    """Check if all strings in a list are composed only of digits.

    Args:
        strings (list[str]): A list of strings to check.

    Returns:
        bool: True if all strings in the list contain only digits; False otherwise.
    """

    return all(string.isdigit() for string in strings)

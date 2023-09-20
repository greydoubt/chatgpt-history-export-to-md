# utils.py

import datetime
import os
import re
import sys
import zipfile
from glob import glob
from pathlib import Path
from typing import Optional

# Checking Python version to ensure compatibility
if sys.version_info < (3, 10):
    raise Exception("Python 3.10 or a more recent version is required.")

# Pre-compiled pattern for disallowed characters in file names
DISALLOWED_CHARS_PATTERN = re.compile(r'[<>:"/\\|?*\n\r\t\f\v]')


def extract_zip(zip_filepath: str) -> None:
    """
    Extract the contents of the specified ZIP file.

    Args:
        zip_filepath (str): The file path of the ZIP file to extract.

    Raises:
        Exception: If any error occurs during the extraction.
    """
    try:
        extract_folder: str = os.path.splitext(os.path.abspath(zip_filepath))[0]

        with zipfile.ZipFile(zip_filepath, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
            print(f"Successfully extracted ZIP file to '{extract_folder}'")
    except Exception as e:
        print(f"An error occurred while extracting the ZIP file: {e}")


def get_most_recent_zip() -> Optional[str]:
    """
    Get the most recent ZIP file from the '~/Downloads' directory.

    Returns:
        Optional[str]: The path to the most recent ZIP file, or None if no ZIP files are found or an error occurs.

    Raises:
        FileNotFoundError: If the 'Downloads' directory or ZIP files are not found.
    """
    try:
        downloads_path = str(Path.home() / "Downloads")

        if not os.path.isdir(downloads_path):
            raise FileNotFoundError(
                f"'Downloads' directory not found: {downloads_path}"
            )

        zip_files: list[str] = glob(os.path.join(downloads_path, "*.zip"))

        if not zip_files:
            raise FileNotFoundError("No ZIP files found in the 'Downloads' directory.")

        return max(zip_files, key=os.path.getctime)
    except Exception as e:
        print(f"An error occurred while looking for the ZIP file: {e}")
        return None


def sanitize_title(title: str) -> str:
    """
    Sanitize the title by replacing disallowed characters with '-'.

    Args:
        title (str): The title to sanitize.

    Returns:
        str: The sanitized title.
    """
    sanitized_title: str = DISALLOWED_CHARS_PATTERN.sub("-", title.strip())
    return sanitized_title


def timestamp_to_str(timestamp: float) -> Optional[str]:
    """
    Convert a Unix timestamp to a formatted string.

    Args:
        timestamp (float): The Unix timestamp to convert.

    Returns:
        Optional[str]: The formatted timestamp as a string, or None if the input is invalid.
    """
    try:
        dt_object = datetime.datetime.utcfromtimestamp(timestamp)
        formatted_timestamp: str = dt_object.strftime("%d %b %Y, %H:%M:%S")
        return formatted_timestamp
    except ValueError as e:
        print(f"Invalid timestamp value: {e}")
        return None


def format_title(title: str, max_length: int = 50) -> str:
    """
    Formats the title to a single line with a specified maximum length. If the title is longer than the maximum
    length, it is truncated and "..." is appended.

    Args:
        title (str): The title to format.
        max_length (int, optional): The maximum allowed length for the title. Defaults to 50.

    Returns:
        str: The formatted title.
    """
    single_line_title: str = " ".join(title.splitlines())
    return (
        single_line_title[:max_length] + "..."
        if len(single_line_title) > max_length
        else single_line_title
    )

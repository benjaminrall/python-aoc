"""Helper utility functions used in the rest of the project."""

import os

def create_dirs(path: str) -> None:
    """Creates all the directories in a given path."""
    # Checks if the path already exists
    if os.path.exists(path):
        return
    
    # Creates the path if it doesn't exist
    accumulated_path = ""
    for d in path.split("/"):
        if d == "":
            continue
        accumulated_path += d + "/"
        if not os.path.exists(accumulated_path):
            os.mkdir(accumulated_path)

def string_replace(string: str, insertion: str, start: int, end: int) -> str:
    """Replaces part of a string with some inserted text."""
    return string[:start] + insertion + string[end:]

def replace_line(string: str, insertion: str, index: int) -> str:
    """Replaces all text in a string from the given index to the end of its line."""
    trimmed = string[index:]
    end = trimmed.find("\n")
    end = len(string) if end == -1 else index + end
    return string_replace(string, insertion, index, end)

def string_remove(string: str, start: int, end: int) -> str:
    """Removes part of a string."""
    return string[:start] + string[end + 1:]

def remove_line(string: str, index: int) -> str:
    """Removes all text in a string from the given index to the end of its line."""
    trimmed = string[index:]
    end = trimmed.find("\n")
    end = len(string) if end == -1 else index + end
    return string_remove(string, index, end)
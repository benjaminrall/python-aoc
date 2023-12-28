from datetime import date
from .constants import URL
import os

def get_day_url(day: int = None, year: int = None) -> str:
    """Returns the URL for AoC for the given day and year."""
    # Gives day and year default values
    if day is None:
        day = date.today().day
    if year is None:
        year = date.today().year
    
    return f"{URL}/{year}/day/{day}"

def get_session() -> str:
    """Returns the current AoC session stored as an environment variable."""
    return os.environ.get("AOC_SESSION")
    
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
    return string[:start] + insertion + string[end:]

def replace_line(string: str, insertion: str, index: int) -> str:
    trimmed = string[index:]
    end = trimmed.find("\n")
    end = len(string) if end == -1 else index + end
    return string_replace(string, insertion, index, end)

def string_remove(string: str, start: int, end: int) -> str:
    return string[:start] + string[end + 1:]

def remove_line(string: str, index: int) -> str:
    trimmed = string[index:]
    end = trimmed.find("\n")
    end = len(string) if end == -1 else index + end
    return string_remove(string, index, end)
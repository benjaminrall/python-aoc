from .utils import get_day_url, get_session, verify_path
from datetime import date
import webbrowser
import requests

def open_day(day: int = None, year: int = None) -> None:
    """Opens the challenge page for a given day and year of AoC in your default browser.
 
    Parameters
    ----------
    day : int, optional
        The day to open, by default the current day.
    year : int, optional
        The year to open, by default the current year.
    """
    webbrowser.open(get_day_url(day, year))

def get_day_input(day: int = None, year: int = None) -> str:
    """Fetches the input for a given day and year of AoC.

    Parameters
    ----------
    day : int, optional
        The day to fetch, by default the current day.
    year : int, optional
        The year to fetch, by default the current year.
    """
    # Checks that the session cookie environment variable exists
    session = get_session()
    if session is None:
        raise Exception(
            "To get input correctly the session cookie must be stored in the 'AOC_SESSION' environment variable."
        )

    # Fetches the website
    input_url = f"{get_day_url(day, year)}/input"
    try:
        response = requests.get(input_url, cookies={'session': session})
    except Exception as e:
        raise Exception(
            "Something went wrong requesting the AoC site. Ensure your session cookie is valid."
        )

    # Catches invalid status code returns from the response
    if response.status_code == 404:
        raise Exception(
            "Cannot find an available input for the given day and year."
        )
    elif response.status_code != 200:
        raise Exception(
            "An error occurred while attempting to fetch the input. " +
            f"Status code: {response.status_code}"
        )

    return response.text

def save_day_input(path: str = None, day: int = None, year: int = None) -> None:
    """Saves the input for a given day and year of AoC to a file called 'input.txt' at the given path.

    Parameters
    ----------
    day : int, optional
        The day to fetch, by default the current day.
    year : int, optional
        The year to fetch, by default the current year.
    """
    # Fills default path and ensures file will be saved as `input.txt`
    if path is None:
        path = f"day-{day if day else date.today().day}/input.txt"
    if not path.endswith("/input.txt"):
        path += ("" if path.endswith("/") else "/") + "input.txt"

    # Gets the day input text
    day_input = get_day_input(day, year)

    # Writes the input to the file 
    verify_path(path[:-10])
    with open(path, "w") as f:
        f.write(day_input)

def create_day():
    pass
from .utils import get_day_url, get_session, create_dirs
from datetime import date
import webbrowser
import requests
from typing import Callable
import os

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
    path: str, optional
        The path to save to, defaults to a folder with the name `day-n`
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
    create_dirs(path[:-10])
    with open(path, "w") as f:
        f.write(day_input)

def copy_template(path: str = None, part: int = 1, day: int = None, year: int = None) -> None:
    """Copies the template AoC code file to a given path.

    Parameters
    ----------
    path : str, optional
        The python file to save to, by default `day-n/main.py`
    """
    # Fills default path and ensures saved file will be a python file
    if path is None:
        path = f"day-{date.today().day}/main.py"
    if not path.endswith(".py"):
        path += ("" if path.endswith("/") else "/") + "main.py"

    # Gets the path of the template file
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.py")
    
    # Creates the path directories 
    try:
        create_dirs(path[:path.rindex("/")])
    except:
        pass
    
    # Copies the template, filling in necessary placeholders
    with open(template_path, "r") as src:
        with open(path, "w") as dest:
            dest.write(src.read().format(
                part = part,
                day = day,
                year = year
            ))

def test_solution(fn: Callable[[str], int], test_result: int, 
                  path: str ="test.txt", verbose: bool = True) -> bool:
    """Tests a solution against a given result.

    Parameters
    ----------
    fn : Callable[[str], int]
        _description_
    test_result : int
        _description_
    path : str, optional
        _description_, by default "test.txt"
    verbose : bool, optional
        _description_, by default True

    Returns
    -------
    bool
        _description_
    """
    if test_result is None:
        if verbose:
            print(f"To test correctly, `test_result` must not be `None`.")
        return False
    result = fn(path)
    passed = result == test_result
    if verbose:
        print(f"Test result: `{result}`", end="")
        print(f", which is " + ("correct." if passed else "incorrect."))
    return passed


def submit(fn: Callable[[str], int], part: int, day: int = None, year: int = None, 
           path: str = "input.txt", test: bool = True, test_path: str = "test.txt", 
           test_result: int = None, verbose: bool = True,) -> bool:
    """Submits the answer generated by a given function for some input.
    By default, attempts to run a test first before submitting to the current session path.

    Parameters
    ----------
    fn : Callable[[str], int]
        The function to call with the path to the input file.
    part : int
        The part of the day to submit to.
    day : int, optional
        The day to submit to, by default the current day.
    year : int, optional
        The yaer to submit to, by default the current year.
    path : str, optional
        Path to the real input file, by default "input.txt"
    test : bool, optional
        Whether to test before submitting, by default True
    test_path : str, optional
        The path to the test input file, by default "test.txt"
    test_result : int, optional
        The expected result to receive from testing.
    verbose : bool, optional
        Whether to test and submit verbosely, by default True

    Returns
    -------
    bool
        Whether the submission was successful.
    """
    # Runs the test on the submitted function
    if test:
        passed = test_solution(fn, test_result, test_path, verbose)
        if not passed:
            if verbose:
                print(f"Test failed, not running on real input.")
            return False
        if verbose:
            print(f"Test successful, running on real input.")
    
    # Runs the real input
    result = fn(path)
    if verbose:
        print(f"Final Result: `{result}`")
        print(f"Attempting to submit day {day}-{year} part {part} to AoC.")
    
    # Checks that the session cookie environment variable exists
    session = get_session()
    if session is None:
        raise Exception(
            "To get input correctly the session cookie must be stored in the 'AOC_SESSION' environment variable."
        )

    # Attempts to submit the result
    result = requests.post(
        f"{get_day_url(day, year)}/answer",
        data={'level': part, 'answer': result},
        cookies={'session': session}
    )
    response = result.text
    
    print(response)
    return True

def create_day():
    pass
from .utils import get_day_url, get_session, create_dirs, replace_line, remove_line, string_remove
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
        The day to open, by default the current day
    year : int, optional
        The year to open, by default the current year
    """
    webbrowser.open(get_day_url(day, year))

def get_day_input(day: int = None, year: int = None) -> str:
    """Fetches the input for a given day and year of AoC.

    Parameters
    ----------
    day : int, optional
        The day to fetch, by default the current day
    year : int, optional
        The year to fetch, by default the current year
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

def save_day_input(day: int = None, year: int = None, path: str = None) -> None:
    """Saves the input for a given day and year of AoC to a file called 'input.txt' at the given path.

    Parameters
    ----------
    day : int, optional
        The day to fetch, by default the current day
    year : int, optional
        The year to fetch, by default the current year
    path: str, optional
        The path to save to, defaults to a folder with the name `day-n`
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

def copy_template(part: int = 1, day: int = None, year: int = None, path: str = None) -> None:
    """Copies the template AoC code file to a given path.

    Parameters
    ----------
    part: int, optional
        The part of the day to create a template for, by default 1
    day: int, optional
        The day to create a template for, by default the current day
    year: int, optional
        The year to create a template for, by default the current year
    path : str, optional
        The python file to save to, by default `day-n/main.py`
    """
    # Fills default path and ensures saved file will be a python file
    if path is None:
        path = f"day-{day if day else date.today().day}/main.py"
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
        The function to call with the path to the test input file
    test_result : int
        The example result to test against
    path : str, optional
        Path to the test input file, by default "test.txt"
    verbose : bool, optional
        Whether to test verbosely, by default True

    Returns
    -------
    bool
        Whether the test was successful.
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
           test_result: int = None, verbose: bool = True) -> bool:
    """Submits the answer generated by a given function for some input.
    By default, attempts to run a test first before submitting to the current session path.

    Parameters
    ----------
    fn : Callable[[str], int]
        The function to call with the path to the input file
    part : int
        The part of the day to submit to
    day : int, optional
        The day to submit to, by default the current day
    year : int, optional
        The year to submit to, by default the current year
    path : str, optional
        Path to the real input file, by default "input.txt"
    test : bool, optional
        Whether to test before submitting, by default True
    test_path : str, optional
        The path to the test input file, by default "test.txt"
    test_result : int, optional
        The expected result to receive from testing
    verbose : bool, optional
        Whether to test and submit verbosely, by default True

    Returns
    -------
    bool
        Whether the submission was successful and the answer was correct.
    """
    # Checks the part is valid
    if part < 1 or part > 2:
        raise Exception(f"Attempted to submit to invalid part number `{part}`.")

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

    # Prints an appropriate response depending on the outcome of the submission
    completed = False
    if "That's the right answer" in response:
        print("Answer correct,", end=" ")
        if part == 1:
            print("saving and moving to part 2...")
        else:
            print("day complete!")
        completed = True
    elif "That's not the right answer" in response:
        print("Answer incorrect, try again.")
    elif "You gave an answer too recently" in response:
        print("Rate limited!", end=" ")
        time_start = response.rindex("You have ")
        time_end = response.rindex("left to wait.")
        print(response[time_start:time_end] + "left.")
    elif "Did you already complete it?" in response:
        print("You have already completed this challenge!")
        completed = True
    elif "[Log In]" in response:
        print("Session cookie is invalid or expired.")
    else:
        print("Something went wrong while submitting: ")
        print(response)

    if completed:
        try:
            # Gets current solution
            main_path = os.path.join(os.path.curdir, "main.py")
            with open(main_path, "r") as f:
                solution_contents = f.read()

            # Formats and saves current solution
            import_i = solution_contents.index("import pyaoc")
            submit_i = solution_contents.index("# Attempt to submit")
            saved_contents = string_remove(solution_contents, submit_i, len(solution_contents))
            saved_contents = remove_line(saved_contents, import_i)
            main_thread = 'if __name__ == "__main__":\n'
            test_print = '    print(f"Test solution: {solve(\'test.txt\')}")\n'
            actual_print = '    print(f"Actual solution: {solve(\'input.txt\')}")\n'
            saved_contents = replace_line(saved_contents, main_thread, len(saved_contents))
            saved_contents = replace_line(saved_contents, test_print, len(saved_contents))
            saved_contents = replace_line(saved_contents, actual_print, len(saved_contents))
            with open(os.path.join(os.path.curdir, f"part{part}.py"), "w") as f:
                f.write(saved_contents)

            # Advances or deletes `main.py` file depending on the current part
            if part == 1:
                part_i = solution_contents.index("PART")
                new_contents = replace_line(solution_contents, "PART = 2", part_i)
                test_i = solution_contents.index("TEST")
                new_contents = replace_line(new_contents, "TEST_RESULT = None", test_i)
                with open(main_path, "w") as f:
                    f.write(new_contents)
            else:
                if os.path.exists(main_path):
                    os.remove(main_path)
        except FileNotFoundError:
            print("Unable to save solution as the `main.py` file", end=" ")
            print("could not be found in the executing directory.")
        except ValueError:
            print("Ensure your file is correctly formatted from the template to allow saving and progression.")
        except Exception as e:
            print(f"Something went wrong while attempting to save the solution: {e}") 
        return True

    return False

def create_test_file(path: str = None) -> None:
    # Fills default path
    if path is None:
        path = f"/test.txt"
    if not path.endswith("/test.txt"):
        path += ("" if path.endswith("/") else "/") + "test.txt"

    # Creates directories
    create_dirs(path[:-9])
    
    # Creates the empty test file
    with open(path, "w") as f:
        f.write("")

def create_day(day: int = None, year: int = None, path: str = None) -> None:
    # Fills default path
    if path is None:
        path = f"day-{day if day else date.today().day}/"
    if not path.endswith("/"):
        path += "/"

    # Opens the day's page
    open_day(day, year)

    # Copies main template file for the day
    copy_template(1, day, year, path)

    # Creates blank test input file
    create_test_file(path)

    # Saves input for the day
    save_day_input(day, year, path)
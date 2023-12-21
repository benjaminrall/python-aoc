from typing import Callable
from datetime import date
from .utils import get_day_url, get_session
import requests

class Session:
    def __init__(self, part: int = 1, day: int = None, year: int = None) -> None:
        self.part = part if part == 1 or part == 2 else 1
        self.day = day if day is not None else date.today().day
        self.year = year if year is not None else date.today().year
        self.test_result = None
    
    def set_test_result(self, test_result) -> None:
        """Sets the test result for the current session"""
        self.test_result = test_result

def test_solution(fn: Callable[[str], int], test_result: int, 
                  path: str ="test.txt", verbose: bool = True) -> bool:
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



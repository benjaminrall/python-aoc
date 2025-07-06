import typer
from typing import Optional, Callable
from datetime import date
import os
import sys
import importlib.util

from . import commands as aoc

# Main Typer application
app = typer.Typer(
    help="A Python CLI and library for interacting with the Advent of Code API."
)

def _load_solve_method(path: str) -> Callable[[str], int]:
    """Attempts to load the 'solve' method from the given Python file path."""
    # Checks that the given path exists
    if not os.path.exists(path):
        print(f"Error: Solution file not found at '{path}'.")
        raise typer.Exit(code=1)
    
    # Creates a module spec from the given path
    spec = importlib.util.spec_from_file_location("solution", path)
    if spec is None:
        print(f"Error: Could not create module spec from '{path}'.")
        raise typer.Exit(code=1)
    
    # Loads the solution module from its spec
    solution_module = importlib.util.module_from_spec(spec)
    sys.modules["solution"] = solution_module

    # Attempts to execute the solution module
    try:
        spec.loader.exec_module(solution_module)
    except Exception as e:
        print(f"Error executing solution file: {e}")
        raise typer.Exit(code=1)

    # Gets the 'solve' function from the module
    if not hasattr(solution_module, 'solve'):
        print(f"Error: No 'solve' method found in '{path}'")
        raise typer.Exit(code=1)
        
    # Returns a reference to the method
    return getattr(solution_module, 'solve')

@app.command(help="Displays the currently saved AoC session token.")
def session():
    session = aoc.get_session()
    if session:
        print(f"Current session token: {session}")
    else:
        print("No session token is currently set.")

@app.command(help="Opens a puzzle page in your default browser.")
def open(
    day: Optional[int] = typer.Argument(None, help="The day to open. Defaults to the current day."),
    year: Optional[int] = typer.Argument(None, help="The year to open. Defaults to the current year."),
):
    aoc.open_day(day, year)
    print(f"Opening puzzle page for year {year or date.today().year}, day {day or date.today().day}...")

@app.command(help="Saves a puzzle's input to a file.")
def save(
    day: Optional[int] = typer.Argument(None, help="The day to save. Defaults to the current day."),
    year: Optional[int] = typer.Argument(None, help="The year to save. Defaults to the current year."),
    path: Optional[str] = typer.Argument(None, help="Directory to save 'input.txt' in. Defaults to 'day-n/'.")
):
    try:
        aoc.save_day_input(day, year, path)
        print("Input saved successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)
    
@app.command(help="Tests a solution function against an expected result.")
def test(
    python_file: str = typer.Argument(..., help="Path to the Python solution file."),
    result: int = typer.Argument(..., help="The expected result for the test case."),
    test_input_path: str = typer.Argument("test.txt", help="Path to the test input file."),
):
    solve_method = _load_solve_method(python_file)
    aoc.test_solution(solve_method, result, test_input_path)

@app.command(help="Submits an answer for a puzzle.")
def submit(
    python_file: str = typer.Argument(..., help="Path to the Python solution file."),
    part: int = typer.Argument(..., help="The puzzle part to submit (1 or 2)."),
    day: Optional[int] = typer.Argument(None, help="The day to submit for. Defaults to the current day."),
    year: Optional[int] = typer.Argument(None, help="The year to submit for. Defaults to the current year."),
    input_path: str = typer.Argument("input.txt", help="Path to the real input file."),
    test_result: Optional[int] = typer.Option(None, help="Expected test result. If provided, runs a test before submitting."),
    test_input_path: str = typer.Option("test.txt", help="Path to the test input file for pre-submission testing."),
):
    solve_method = _load_solve_method(python_file)
    try:
        aoc.submit(
            fn=solve_method,
            part=part,
            day=day,
            year=year,
            path=input_path,
            test=test_result is not None,
            test_path=test_input_path,
            test_result=test_result,
            verbose=True
        )
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)
    
@app.command(help="Creates a full day's folder structure including puzzle input and a template Python file.")
def create(
    day: Optional[int] = typer.Argument(None, help="The day to create. Defaults to the current day."),
    year: Optional[int] = typer.Argument(None, help="The year to create. Defaults to the current year."),
    path: Optional[str] = typer.Argument(None, help="The base path to create the 'day-n/' folder in.")
):
    aoc.create_day(day, year, path)
    print("Day structure created successfully.")

def main():
    app()

if __name__ == "__main__":
    main()
# Python Advent of Code 🎄

A Python CLI and library for interacting with the [Advent of Code](https://adventofcode.com/) API.

## Key Features

- 🌐 Opens the daily puzzle page in your browser
- 🚀 Downloads your personalised puzzle inputs
- 📂 Generates new solution files from a template
- ✅ Tests and directly submits your solutions

## Installation

To use the project, you can simply install it using `pip`:

```sh
pip install python-aoc
```

It can then be used in the command line and imported as a library with `pyaoc`.

## Configuration

To interact with the Advent of Code API, you must provide your session token. This tool reads the token from an environment variable named `AOC_SESSION`, which must be set before use.

To verify that your session cookie is set up correctly, you can display it using the following command:

```sh
pyaoc session
```

## Quick Start

The most common workflow is to create, test, and submit a solution.

1. **Create the files for a new day**:

   The following command will create a `day-5/` directory, download the input into `day-5/input.txt`, create a `day-5/test.txt` file to hold a test input, and create a `day-5/main.py` script file from the default `python-aoc` template:

   ```sh
   pyaoc create 5 2025
   ```

2. **Test your solution against a known answer**:

   Once you have completed your solution to the puzzle, written in a `solve` function which takes in the path to an input file, you can test it against a known answer for an example case in `test.txt`:

   ```sh
   # Assuming the example answer is 123
   pyaoc test day-5/main.py 123 --test-input-path day-5/test.txt
   ```

3. **Submit your final solution**:

   Then, the final solution for the specified part can be submitted using the `submit` command:

   ```sh
   pyaoc submit day-5/main.py 1 --day 5 --year 2025 --input-path day-5/input.txt
   ```

For the complete list of CLI commands and their arguments, run `pyaoc --help`.

## Library Usage

You can also import and use the core functions in your own Python scripts:

```py
import pyaoc

# Sets the session token for this script
pyaoc.set_session("your-session-token")

try:
    # Get puzzle input for Day 1, 2023
    puzzle_input = pyaoc.get_day_input(day=1, year=2023)
    print(puzzle_input[:50]) # Prints the first 50 characters
except Exception as e:
    print(f"An error occurred: {e}")
```

## Development Setup

This project uses [uv](https://github.com/astral-sh/uv) as a package and virtual environment manager. To set up the project for development, follow these steps:

1. **Clone the repository**:

   ```sh
   git clone https://github.com/benjaminrall/python-aoc.git
   cd python-aoc
   ```

2. **Create the virtual environment using [uv](https://github.com/astral-sh/uv)**:

   ```sh
   uv venv
   ```

3. **Install the project in editable mode**:

   ```sh
   uv pip install -e .
   ```

   This will allow use of the `pyaoc` command such that any changes made to the source code will be immediately reflected.

## License
This project is licensed under the **MIT License**. See the [`LICENSE`](./LICENSE) file for details.


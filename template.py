# Useful imports
from pyaoc import Session
import math
import numpy as np

# Placeholders to be filled when copying the template
PART = {part}
DAY = {day}
YEAR = {year}

# The expected result from the test input, if using a test input
TEST_RESULT = None

# Gets and sets up the pyaoc session
session = Session(PART, DAY, YEAR)
session.set_test_result(TEST_RESULT)

# Method to solve the input stored in a given file name
def solve(filename: str) -> int:
    # --- INPUT HANDLING ---
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    print(lines)

    # --- SOLUTION CODE ---
    return None

# Submit the current solve method
session.submit(solve)
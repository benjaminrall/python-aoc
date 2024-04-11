# Useful imports
import pyaoc
import math
import numpy as np
from functools import cache
from collections import defaultdict

# Placeholders to be filled when copying the template
PART = {part}
DAY = {day}
YEAR = {year}

# The expected result from the test input, if using a test input
TEST_RESULT = None

# Method to solve the input stored in a given file name
def solve(filename: str) -> int:
    # --- SOLUTION CODE ---
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    print(lines)

    return None

# Attempt to submit the current solve method
pyaoc.submit(
    solve, PART, DAY, YEAR, 
    test_result=TEST_RESULT,
    test=True
)
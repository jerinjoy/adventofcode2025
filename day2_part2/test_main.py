"""Test suite for main.py to verify correctness of optimizations."""

import pytest
from main import calculate_sum_of_invalid_ids

# Dictionary mapping input files to their expected sum of invalid IDs
EXPECTED_RESULTS = {
    "test_input.txt": 4174379265,
    "test_input2.txt": 2252,
    "puzzle_input.txt": 31755323497,
}


@pytest.mark.parametrize("input_file,expected_sum", EXPECTED_RESULTS.items())
def test_sum_of_invalid_ids(input_file, expected_sum):
    """Test that the sum of invalid IDs matches the expected baseline."""
    with open(input_file, "r") as f:
        content = f.read()

    result = calculate_sum_of_invalid_ids(content)
    assert result == expected_sum, f"Expected {expected_sum}, got {result}"

import pytest
from main import process_file


TEST_CASES = [
    {
        "input_file": "test_input.txt",
        "num_batteries": 2,
        "expected_joltage": 357,
    },
    {
        "input_file": "puzzle_input.txt",
        "num_batteries": 2,
        "expected_joltage": 17321,
    },
    {
        "input_file": "test_input.txt",
        "num_batteries": 12,
        "expected_joltage": 3121910778619,
    },
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_input_files(test_case):
    """Test input files with their configurations."""
    total_joltage = process_file(test_case["input_file"], test_case["num_batteries"])
    assert total_joltage == test_case["expected_joltage"], (
        f"File '{test_case['input_file']}' with {test_case['num_batteries']} batteries: "
        f"expected total joltage={test_case['expected_joltage']}, got {total_joltage}"
    )


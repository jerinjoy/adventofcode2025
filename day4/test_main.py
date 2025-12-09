import pytest
from main import count_elements_with_fewer_than_4_surrounding_ones, count_elements_that_can_be_removed


TEST_CASES_FEWER_THAN_4 = [
    {
        "input_file": "test_input.txt",
        "expected_count": 13,
    },
    {
        "input_file": "puzzle_input.txt",
        "expected_count": 1478,
    },
]

TEST_CASES_CAN_BE_REMOVED = [
    {
        "input_file": "test_input.txt",
        "expected_count": 43,
    },
    {
        "input_file": "puzzle_input.txt",
        "expected_count": 9120,
    },
]


@pytest.mark.parametrize("test_case", TEST_CASES_FEWER_THAN_4)
def test_input_files(test_case):
    """Test input files with their configurations."""
    count = count_elements_with_fewer_than_4_surrounding_ones(test_case["input_file"])
    assert count == test_case["expected_count"], (
        f"File '{test_case['input_file']}': "
        f"expected count={test_case['expected_count']}, got {count}"
    )


@pytest.mark.parametrize("test_case", TEST_CASES_CAN_BE_REMOVED)
def test_count_elements_that_can_be_removed(test_case):
    """Test count_elements_that_can_be_removed function."""
    count = count_elements_that_can_be_removed(test_case["input_file"])
    assert count == test_case["expected_count"], (
        f"File '{test_case['input_file']}': "
        f"expected count={test_case['expected_count']}, got {count}"
    )


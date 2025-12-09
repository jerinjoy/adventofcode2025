import pytest
from main import count_fresh_ingredients


TEST_CASES = [
    {
        "input_file": "test_input.txt",
        "expected_count": 3,
        "expected_total_elements": 14,
    },
    {
        "input_file": "puzzle_input.txt",
        "expected_count": 681,
        "expected_total_elements": 348820208020395,
    },
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_count_fresh_ingredients(test_case):
    """Test count_fresh_ingredients function."""
    count, total_elements = count_fresh_ingredients(test_case["input_file"])
    assert count == test_case["expected_count"], (
        f"File '{test_case['input_file']}': "
        f"expected count={test_case['expected_count']}, got {count}"
    )
    assert total_elements == test_case["expected_total_elements"], (
        f"File '{test_case['input_file']}': "
        f"expected total_elements={test_case['expected_total_elements']}, got {total_elements}"
    )


import argparse


class Range:
    def __init__(self, start: int, end: int):
        # Store original values
        self.original_start = start
        self.original_end = end

    def first(self) -> int:
        """Return the first number in the range."""
        return self.original_start

    def last(self) -> int:
        """Return the last number in the range."""
        return self.original_end

    def contains(self, number: int) -> bool:
        """Check if a given number is in the range (inclusive)."""
        return self.original_start <= number <= self.original_end

    def __contains__(self, number: int) -> bool:
        """Allow using 'in' operator: number in range."""
        return self.contains(number)

    def __repr__(self) -> str:
        return f"[{self.original_start}-{self.original_end}]"


def valid_set_sizes(number: int) -> list[int]:
    """Return the valid sizes of sets given a number.

    Returns the sizes that are factors of the length of the number,
    but only those that are at most half the length.

    Examples:
        11 -> [1]
        123 -> [1]
        1234 -> [1, 2]
        1188511880 -> [1, 2, 5]
    """
    num_str = str(number)
    length = len(num_str)
    max_size = length // 2

    # Find all factors of the length that are at most half the length
    factors = []
    for i in range(1, max_size + 1):
        if length % i == 0:
            factors.append(i)

    return factors


def divide_into_components(number: int, set_size: int) -> list[int]:
    """Divide a number into components of the given set size.

    Args:
        number: The number to divide
        set_size: The size of each component

    Returns:
        A list of integers, each representing a component of the given size.

    Examples:
        446443 with set_size 1 -> [4, 4, 6, 4, 4, 3]
        446443 with set_size 2 -> [44, 64, 43]
    """
    num_str = str(number)
    components = []
    for i in range(0, len(num_str), set_size):
        component = num_str[i : i + set_size]
        components.append(int(component))
    return components


def all_components_same(components: list[int]) -> bool:
    """Check if all components in the list are the same.

    Args:
        components: A list of integers

    Returns:
        True if all components are the same, False otherwise.

    Examples:
        [4, 4, 4] -> True
        [4, 4, 6, 4, 4, 3] -> False
        [44, 44, 44] -> True
    """
    if not components:
        return True
    first = components[0]
    return all(component == first for component in components)


def parse_ranges(content: str) -> list[Range]:
    ranges = []
    parts = content.strip().split(",")
    for part in parts:
        start, end = map(int, part.split("-"))
        ranges.append(Range(start, end))
    return ranges


def calculate_sum_of_invalid_ids(content: str, verbose: bool = False) -> int:
    """Calculate the sum of invalid IDs from the given content.

    Args:
        content: The input string containing comma-separated ranges
        verbose: If True, print debug information

    Returns:
        The sum of all invalid IDs
    """
    ranges = parse_ranges(content)
    invalid_ids = []

    for range in ranges:
        current_number = range.first()
        while current_number <= range.last():
            for size in valid_set_sizes(current_number):
                components = divide_into_components(current_number, size)
                if all_components_same(components):
                    if verbose:
                        print(f"Number {current_number} is invalid")
                    invalid_ids.append(current_number)
                    break

            current_number = current_number + 1

    if verbose:
        print(f"Invalid IDs: {invalid_ids}")
        print(f"Sum of invalid IDs: {sum(invalid_ids)}")

    return sum(invalid_ids)


def main():
    parser = argparse.ArgumentParser(description="Advent of Code Day 2 Part 2")
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input file"
    )
    args = parser.parse_args()

    with open(args.input, "r") as f:
        content = f.read()

    calculate_sum_of_invalid_ids(content, verbose=True)


if __name__ == "__main__":
    main()

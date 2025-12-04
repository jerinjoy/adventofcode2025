import argparse


def has_even_digits(number: int) -> bool:
    """Check if a number has an even number of digits."""
    return len(str(number)) % 2 == 0


def next_even_digit_number(number: int) -> int:
    """Find the next number (>= number) that has an even number of digits."""
    if has_even_digits(number):
        return number

    num_digits = len(str(number))
    # If odd number of digits, round up to next power of 10 with even digits
    if num_digits % 2 == 1:
        # Next even digit count is num_digits + 1
        return 10**num_digits
    return number


def prev_even_digit_number(number: int) -> int:
    """Find the largest number (<= number) that has an even number of digits."""
    if has_even_digits(number):
        return number

    num_digits = len(str(number))
    # If odd number of digits, the largest number with even digits is
    # the previous power of 10 with even digits minus 1
    if num_digits % 2 == 1:
        # Previous even digit count is num_digits - 1
        if num_digits == 1:
            # For 1-digit numbers, there's no smaller number with even digits
            # The smallest number with even digits is 10 (2 digits)
            # So we return the number itself (can't find a valid smaller one)
            return number
        # For numbers with 3, 5, 7, etc. digits, return the largest number
        # with (num_digits - 1) digits, which is 10^(num_digits-1) - 1
        return 10 ** (num_digits - 1) - 1
    return number


class Range:
    def __init__(self, start: int, end: int):
        # Store original values
        self.original_start = start
        self.original_end = end

        # Adjust to have even number of digits
        self.start = next_even_digit_number(start)
        self.end = prev_even_digit_number(end)

        # Mark as invalid if start >= end
        self.invalid = self.start >= self.end

    def first(self) -> int:
        """Return the first number in the range."""
        return self.start

    def last(self) -> int:
        """Return the last number in the range."""
        return self.end

    def contains(self, number: int) -> bool:
        """Check if a given number is in the range (inclusive)."""
        return self.start <= number <= self.end

    def __contains__(self, number: int) -> bool:
        """Allow using 'in' operator: number in range."""
        return self.contains(number)

    def __repr__(self) -> str:
        status = " INVALID" if self.invalid else ""
        return f"[{self.original_start}-{self.original_end}] -> [{self.start}-{self.end}]{status}"


def parse_ranges(content: str) -> list[Range]:
    ranges = []
    parts = content.strip().split(",")
    for part in parts:
        start, end = map(int, part.split("-"))
        ranges.append(Range(start, end))
    return ranges


def main():
    parser = argparse.ArgumentParser(description="Advent of Code Day 2")
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input file"
    )
    args = parser.parse_args()

    with open(args.input, "r") as f:
        content = f.read()

    invalid_ids = []

    ranges = parse_ranges(content)
    for range in ranges:
        print(f"Inspecting range: {range}")
        if range.invalid:
            print("\tSkipping range because it is invalid")
            continue

        current_number = range.first()

        while current_number <= range.last():
            current_number_string = str(current_number)
            first_half = current_number_string[: len(current_number_string) // 2]
            number_to_check = int(first_half + first_half)
            if number_to_check >= range.first() and number_to_check <= range.last():
                print(f"\tNumber {number_to_check} is invalid")
                invalid_ids.append(number_to_check)
            next_half = int(first_half) + 1
            current_number = int(str(next_half) + str(next_half))

    print(f"Invalid IDs: {invalid_ids}")
    print(f"Sum of invalid IDs: {sum(invalid_ids)}")


if __name__ == "__main__":
    main()

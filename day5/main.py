import argparse
import logging


class FreshRange:
    """
    Represents a range of numbers (inclusive of both first and last).
    """
    
    def __init__(self, first: int, last: int):
        """
        Initialize a FreshRange.
        
        Args:
            first: The first number in the range (inclusive)
            last: The last number in the range (inclusive)
        """
        self.first = first
        self.last = last
    
    def contains(self, number: int) -> bool:
        """
        Check if a number is part of this range.
        
        Args:
            number: The number to check
        
        Returns:
            True if the number is in the range (inclusive), False otherwise
        """
        return self.first <= number <= self.last
    
    def count(self) -> int:
        """
        Return the number of elements in this range.
        
        Returns:
            The count of elements (inclusive of both first and last)
        """
        return self.last - self.first + 1
    
    def overlaps(self, other: 'FreshRange') -> bool:
        """
        Check if this range overlaps with another range.
        
        Args:
            other: Another FreshRange to check against
        
        Returns:
            True if the ranges overlap, False otherwise
        """
        return not (self.last < other.first or self.first > other.last)
    
    def merge(self, other: 'FreshRange') -> 'FreshRange':
        """
        Merge this range with another overlapping range.
        
        Args:
            other: Another FreshRange to merge with
        
        Returns:
            A new FreshRange that encompasses both ranges
        """
        return FreshRange(min(self.first, other.first), max(self.last, other.last))
    
    def __repr__(self) -> str:
        return f"FreshRange({self.first}, {self.last})"


def merge_ranges(ranges: list[FreshRange]) -> list[FreshRange]:
    """
    Merge overlapping ranges in a list.
    
    Args:
        ranges: List of FreshRange objects
    
    Returns:
        List of merged FreshRange objects with no overlaps
    """
    if not ranges:
        return []
    
    # Sort ranges by first number
    sorted_ranges = sorted(ranges, key=lambda r: r.first)
    merged = [sorted_ranges[0]]
    
    for current_range in sorted_ranges[1:]:
        last_merged = merged[-1]
        
        # If current range overlaps with the last merged range, merge them
        if last_merged.overlaps(current_range):
            merged[-1] = last_merged.merge(current_range)
        else:
            # No overlap, add as a new range
            merged.append(current_range)
    
    return merged


def count_fresh_ingredients(input_file: str) -> tuple[int, int]:
    """
    Process an input file and return the count of fresh ingredients and total range elements.
    
    Args:
        input_file: Path to the input file
    
    Returns:
        Tuple of (count of numbers in ranges, total number of elements in all ranges)
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # First, read all ranges (before blank line)
    ranges = []
    numbers = []
    found_blank_line = False
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines (blank line separator)
        if not line:
            found_blank_line = True
            continue
        
        # Parse ranges (before blank line)
        if not found_blank_line:
            # Parse range in format "first-last"
            if '-' in line:
                parts = line.split('-')
                if len(parts) == 2:
                    try:
                        first = int(parts[0])
                        last = int(parts[1])
                        ranges.append(FreshRange(first, last))
                    except ValueError:
                        logging.warning(f"Invalid range format: {line}")
        
        # After blank line, we have numbers to check
        else:
            try:
                number = int(line)
                numbers.append(number)
            except ValueError:
                logging.warning(f"Invalid number format: {line}")
    
    # Sort and merge all ranges at once
    merged_ranges = merge_ranges(ranges)
    logging.debug(f"Final merged ranges: {merged_ranges}")
    
    # Count how many numbers fall into any of the merged ranges
    count = 0
    for number in numbers:
        for range_obj in merged_ranges:
            # Since ranges are sorted by first number, if we've passed all possible ranges, stop
            if range_obj.first > number:
                break
            if range_obj.contains(number):
                count += 1
                logging.debug(f"Number {number} is in range {range_obj}")
                break  # Number can only be in one range (since ranges don't overlap)
    
    # Calculate total number of elements in all ranges
    total_elements = sum(range_obj.count() for range_obj in merged_ranges)
    
    return count, total_elements


def main():
    parser = argparse.ArgumentParser(description="Day 5 solution")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input text file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (show intermediate messages)",
    )
    args = parser.parse_args()
    
    # Configure logging based on verbose flag
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    else:
        logging.basicConfig(level=logging.WARNING, format="%(message)s")
    
    count, total_elements = count_fresh_ingredients(args.input)
    # Print final count (always printed)
    print(f"\nTotal fresh ingredients: {count}")
    print(f"Total elements in ranges: {total_elements}")


if __name__ == "__main__":
    main()

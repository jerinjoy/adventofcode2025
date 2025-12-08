import argparse
from dataclasses import dataclass
from re import S
from typing import List, Tuple


@dataclass
class NumberWithPosition:
    """Represents a number with its original position in the unsorted list."""
    value: int
    original_position: int


class BatteryBank:
    """Represents a battery bank with numbers in original and sorted order."""
    
    def __init__(self, line: str):
        """
        Initialize a BatteryBank from a line of digits.
        
        Args:
            line: A string of digits (e.g., "987654321111111")
        """
        # Parse each digit as an integer
        self.original_order: List[int] = [int(digit) for digit in line.strip()]
        
        # Track the number of elements
        self.num_elements: int = len(self.original_order)
        
        # Create sorted list with original positions
        # First, create tuples of (value, original_index)
        indexed_numbers = [
            NumberWithPosition(value=num, original_position=i)
            for i, num in enumerate(self.original_order)
        ]
        
        # Sort by value in reverse order, and for duplicates sort by original_position in ascending order
        self.sorted_order: List[NumberWithPosition] = sorted(
            indexed_numbers,
            key=lambda x: (-x.value, x.original_position)
        )


def find_max_valid_battery(
    sorted_order: List[NumberWithPosition], num_elements: int, n: int, minimum_original_position: int
) -> int | None:
    """
    Find the battery with the largest value that has n batteries after it in the original list.
    
    Args:
        sorted_order: List of batteries sorted by value (descending) and original_position (ascending)
        num_elements: Total number of elements in the original order
        n: Number of batteries that must come after this battery in the original list
        
    Returns:
        The index of the battery with maximum value that satisfies the condition, or None if no valid battery found
    """
    max_value = -1
    max_index = None
    
    # print(f"Looking for max valid battery with {n} batteries after it in sorted order: {sorted_order}")
    
    for i, battery in enumerate(sorted_order):
        # Check if there are at least n elements after this battery's position
        # If battery is at position i, there are (num_elements - i - 1) elements after it
        if battery.original_position >= minimum_original_position and num_elements - battery.original_position - 1 >= n:
            # Since sorted_order is sorted by value descending, the first valid one is the max
            # But we'll check all to be explicit and ensure we get the maximum
            if battery.value > max_value:
                max_value = battery.value
                max_index = i
    return max_index


def process_bank_line(line: str, num_batteries: int = 2) -> List[int]:
    """
    Process a single bank line and return the enabled battery values.
    
    Args:
        line: A string of digits representing a battery bank
        num_batteries: Number of batteries to enable (default: 2)
        
    Returns:
        A list of battery values in order
    """
    bank = BatteryBank(line)
    enabled_batteries = []
    minimum_original_position = 0

    while len(enabled_batteries) < num_batteries:
        # print(f"Sorted order: {bank.sorted_order}")
        battery_index = find_max_valid_battery(
            bank.sorted_order, bank.num_elements, num_batteries - len(enabled_batteries) - 1, minimum_original_position
        )
        if battery_index is None:
            raise ValueError(f"No valid battery found for {num_batteries} batteries")
        
        # Add the battery to enabled list and remove it from sorted order
        valid_battery = bank.sorted_order[battery_index]
        enabled_batteries.append(valid_battery)
        bank.sorted_order.pop(battery_index)
        minimum_original_position = valid_battery.original_position
        print(f"Added battery: {valid_battery.value} at position {valid_battery.original_position} in original order")

    if len(enabled_batteries) != num_batteries:
        raise ValueError(f"Expected {num_batteries} batteries, got {len(enabled_batteries)}")
    
    sorted_enabled_batteries = sorted(enabled_batteries, key=lambda x: x.original_position)
    return [battery.value for battery in sorted_enabled_batteries]

def process_file(input_file: str, num_batteries: int = 2) -> int:
    """
    Process an input file and return the total joltage.
    
    Args:
        input_file: Path to the input file
        num_batteries: Number of batteries to enable (default: 2)
        
    Returns:
        Total joltage across all banks
    """
    total_battery_value = 0
    with open(input_file, "r") as f:
        for line in f:
            if line.strip():  # Skip empty lines
                enabled_batteries = process_bank_line(line, num_batteries)
                
                # Calculate joltage: each battery contributes its value * 10^(position from right)
                joltage = 0
                for i, battery_value in enumerate(enabled_batteries):
                    power = len(enabled_batteries) - 1 - i
                    joltage += battery_value * (10 ** power)
                
                total_battery_value += joltage
    
    return total_battery_value


def main():
    parser = argparse.ArgumentParser(description="Day 3 solution")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input text file",
    )
    parser.add_argument(
        "--batteries",
        type=int,
        default=2,
        help="Number of batteries to enable (default: 2)",
    )
    args = parser.parse_args()
    
    total_battery_value = 0
    with open(args.input, "r") as f:
        for line in f:
            if line.strip():  # Skip empty lines
                print(f"\nProcessing bank: {line.strip()}")
                enabled_batteries = process_bank_line(line, args.batteries)
                
                # Calculate joltage: each battery contributes its value * 10^(position from right)
                joltage = 0
                for i, battery_value in enumerate(enabled_batteries):
                    power = len(enabled_batteries) - 1 - i
                    joltage += battery_value * (10 ** power)
                
                print(f"Enabled batteries: {enabled_batteries}")
                print(f"Joltage: {joltage}")
                total_battery_value += joltage

    print(f"\nTotal joltage: {total_battery_value}")

if __name__ == "__main__":
    main()

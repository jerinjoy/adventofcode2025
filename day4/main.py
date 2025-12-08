import argparse
import logging


def count_surrounding_ones_at_index(above_line: list[int], current_line: list[int], below_line: list[int], index: int) -> int:
    """
    Count the number of surrounding 1s at a specific index in the current line.
    
    Args:
        above_line: The line above the current line
        current_line: The line containing the element
        below_line: The line below the current line
        index: The index in current_line to check
    
    Returns:
        Count of surrounding 1s (8 neighbors)
    """
    count = 0
    # Above
    if above_line[index] == 1:
        count += 1
    # Below
    if below_line[index] == 1:
        count += 1
    # Left
    if current_line[index - 1] == 1:
        count += 1
    # Right
    if current_line[index + 1] == 1:
        count += 1
    # Top-left
    if above_line[index - 1] == 1:
        count += 1
    # Top-right
    if above_line[index + 1] == 1:
        count += 1
    # Bottom-left
    if below_line[index - 1] == 1:
        count += 1
    # Bottom-right
    if below_line[index + 1] == 1:
        count += 1
    
    return count


def count_surrounding_ones(above_line: list[int], current_line: list[int], below_line: list[int]) -> list[tuple[int, int]]:
    """
    Process the middle line (current_line) and count surrounding 1s for each element that is 1.
    Skips the first and last elements (buffer elements we added).
    
    Args:
        above_line: The line above the current line
        current_line: The line being processed
        below_line: The line below the current line
    
    Returns:
        List of tuples (original_index, count) for each element that is 1, where count is the number of surrounding 1s
    """
    results = []
    
    # Process elements in current line (skip padding: indices 1 to len-2)
    # Only consider elements that came from the file
    for j in range(1, len(current_line) - 1):
        if current_line[j] == 1:
            count = count_surrounding_ones_at_index(above_line, current_line, below_line, j)
            original_index = j - 1
            logging.debug(f"  Element at position {original_index} (original index): {count} surrounding 1s")
            results.append((original_index, count))
    
    return results


# Helper function to convert line to array: @ = 1, . = 0
# Adds a 0 at the beginning and end of each array
def line_to_array(line: str) -> list[int]:
    arr = [1 if char == '@' else 0 for char in line.strip()]
    return [0] + arr + [0]

def count_elements_with_fewer_than_4_surrounding_ones(input_file: str) -> int:
    """
    Process an input file and return the count of elements with fewer than 4 surrounding 1s.
    
    Args:
        input_file: Path to the input file
    
    Returns:
        Count of elements with fewer than 4 surrounding 1s
    """
    # Process file line by line, keeping only current, previous, and next in memory
    with open(input_file, 'r') as f:
        # Get first line to determine array length
        first_line = f.readline().strip()
        if not first_line:
            return 0
        
        # Array length after adding padding (original length + 2 for beginning and end)
        array_length = len(first_line) + 2
        empty_array = [0] * array_length
        
        # Counter for elements with fewer than 4 surrounding 1s
        count_fewer_than_4 = 0
        
        # Convert first line
        previous_line = None
        current_line = line_to_array(first_line)
        
        line_number = 1
        
        # Process first line
        logging.debug(f"\nProcessing line {line_number}:")
        logging.debug(f"Above: {empty_array}")
        logging.debug(f"Current: {current_line}")
        
        # Peek ahead for next line
        next_line_str = f.readline().strip()
        if next_line_str:
            next_line = line_to_array(next_line_str)
            logging.debug(f"Below: {next_line}")
        else:
            next_line = None
            logging.debug(f"Below: {empty_array}")
        
        # Process elements in current line
        above_line = empty_array
        below_line = next_line if next_line is not None else empty_array
        results = count_surrounding_ones(above_line, current_line, below_line)
        for original_index, count in results:
            if count < 4:
                count_fewer_than_4 += 1
        
        # Process remaining lines
        while True:
            # Move to next line
            previous_line = current_line
            current_line = next_line
            
            # If no more lines, we're done
            if current_line is None:
                break
            
            line_number += 1
            
            # Peek ahead for next line
            next_line_str = f.readline().strip()
            if next_line_str:
                next_line = line_to_array(next_line_str)
            else:
                next_line = None
            
            # Process current line
            logging.debug(f"\nProcessing line {line_number}:")
            logging.debug(f"Above: {previous_line}")
            logging.debug(f"Current: {current_line}")
            
            if next_line is not None:
                logging.debug(f"Below: {next_line}")
            else:
                logging.debug(f"Below: {empty_array}")
            
            # Process elements in current line
            above_line = previous_line
            below_line = next_line if next_line is not None else empty_array
            results = count_surrounding_ones(above_line, current_line, below_line)
            for original_index, count in results:
                if count < 4:
                    count_fewer_than_4 += 1
    
    return count_fewer_than_4

def count_elements_that_can_be_removed(input_file: str) -> int:
    """
    Process an input file and return the count of elements that can be removed.
    Elements with fewer than 4 surrounding ones are removed in multiple passes
    until no more can be removed.
    
    Args:
        input_file: Path to the input file
    
    Returns:
        Count of elements that can be removed
    """
    # Read entire file into a 2D array
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return 0
    
    # Convert each line to array (adds padding at beginning and end)
    grid = []
    for line in lines:
        if line.strip():  # Skip empty lines
            grid.append(line_to_array(line))
    
    if not grid:
        return 0
    
    # Get array length (all lines should have same length after padding)
    array_length = len(grid[0])
    empty_array = [0] * array_length
    
    # Add buffer lines above and below
    grid_with_buffers = [empty_array] + grid + [empty_array]
    
    # Now grid_with_buffers is a 2D array with:
    # - Buffer line at the top (index 0)
    # - Original data lines (indices 1 to len(grid))
    # - Buffer line at the bottom (index len(grid) + 1)
    # - Each line has padding 0s at the beginning and end
    
    total_removed = 0
    
    # Run multiple passes until no more elements are removed
    while True:
        removed_this_pass = 0
        # Track positions to remove (we'll remove them after scanning to avoid modifying while iterating)
        positions_to_remove = []
        
        # Iterate through data lines (skip buffer lines at top and bottom)
        # Lines 1 to len(grid) are the actual data
        for i in range(1, len(grid_with_buffers) - 1):
            current_line = grid_with_buffers[i]
            above_line = grid_with_buffers[i - 1]
            below_line = grid_with_buffers[i + 1]
            
            # Iterate through elements in current line (skip padding at start and end)
            for j in range(1, len(current_line) - 1):
                if current_line[j] == 1:
                    count = count_surrounding_ones_at_index(above_line, current_line, below_line, j)
                    if count < 4:
                        positions_to_remove.append((i, j))
        
        # Remove marked elements
        for i, j in positions_to_remove:
            grid_with_buffers[i][j] = 0
            removed_this_pass += 1
        
        total_removed += removed_this_pass
        
        # If no elements were removed this pass, we're done
        if removed_this_pass == 0:
            break
    
    return total_removed

def main():
    parser = argparse.ArgumentParser(description="Day 4 solution")
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
    
    count_fewer_than_4 = count_elements_with_fewer_than_4_surrounding_ones(args.input)
    # Print final count (always printed)
    print(f"\nTotal elements with fewer than 4 surrounding 1s: {count_fewer_than_4}")

    count_numer_of_elements_that_can_be_removed = count_elements_that_can_be_removed(args.input)
    print(f"\nTotal elements that can be removed: {count_numer_of_elements_that_can_be_removed}")

if __name__ == "__main__":
    main()

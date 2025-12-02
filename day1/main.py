import argparse


def main():
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("--input", help="Input file", required=True)
    args = vars(parser.parse_args())

    number_of_zeros_seen = 0
    dial_position = 50

    with open(args["input"], "r") as file:
        for line in file:
            print("\nrotation: ", line.rstrip())
            direction = line[0]
            steps = int(line[1:])

            if steps % 100 != steps:
                print(
                    f"{steps / 100} rotations of the dial back to the same position. incrementing number_of_zeros_seen by {steps / 100}"
                )
                number_of_zeros_seen += int(steps / 100)
                steps = steps % 100

            if direction == "R":
                if dial_position + steps > 100:
                    print(
                        "dial_position + steps > 100. incrementing number_of_zeros_seen by 1"
                    )
                    number_of_zeros_seen += 1
                dial_position += steps
                dial_position = dial_position % 100
            elif direction == "L":
                if dial_position != 0 and dial_position - steps < 0:
                    print(
                        "dial_position - steps < 0. incrementing number_of_zeros_seen by 1"
                    )
                    number_of_zeros_seen += 1
                dial_position += 100 - steps
                dial_position = dial_position % 100

            if dial_position == 0:
                number_of_zeros_seen += 1

            print("dial_position: ", dial_position)
            print("number_of_zeros_seen: ", number_of_zeros_seen)

    print("Number of zeros seen: ", number_of_zeros_seen)


if __name__ == "__main__":
    main()

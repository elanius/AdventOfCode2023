import sys
from typing import Dict, Tuple, List

all_syms = set()
valid_syms = set(['&', '@', '-', '$', '#', '+', '/', '%', '*', '='])
valid_numbers = set()
invalid_numbers = set()
gear: Dict[Tuple[int, int], List[int]] = dict()


def find_number(line, index):
    while index < len(line):
        if line[index].isdigit():
            return index
        else:
            index += 1

    return None


def read_number(line, index):
    str_number = ""
    while line[index].isdigit():
        str_number += line[index]
        index += 1

    return int(str_number), index, len(str_number)


def check_number(number, lines, line_index, index, length):
    for x in range(index - 1, index + length + 1):
        for y in range(line_index - 1, line_index + 2):
            if x < 0 or y < 0 or y >= len(lines) or x >= len(lines[y]):
                continue

            try:
                symbol: str = lines[y][x]
                all_syms.add(symbol)
                if symbol in valid_syms:
                    if symbol == '*':
                        if (x, y) in gear:
                            gear[(x, y)].append(number)
                        else:
                            gear[(x, y)] = [number]

                    return True
                else:
                    continue
            except IndexError:
                print(f"IndexError: {x}, {y}, {lines[y]}")
                raise

    return False


def main():
    sum = 0
    if len(sys.argv) != 2:
        print("Usage: python gear_ratios.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    line_index = 0

    # Read the input file
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        index = 0
        while (index := find_number(line, index)) is not None:
            number, index, length = read_number(line, index)
            if check_number(number, lines, line_index, index-length, length):
                # print(f"Found number: {number}")
                valid_numbers.add(number)
                sum += number
            else:
                # print(f"Found number: {number} but it is not valid")
                invalid_numbers.add(number)
                pass

        line_index += 1

    print(f"Final sum from file: {filename} is {sum}")
    # print(f"Symbols: {[s for s in all_syms if s.isdigit() is False]}")
    # print(f"Valid numbers: {sorted(valid_numbers)}")
    # print(f"Invalid numbers: {sorted(invalid_numbers)}")

    gear_sum = 0
    for point, numbers in gear.items():
        if len(numbers) == 2:
            gear_sum += numbers[0] * numbers[1]
            print(f"Found gear at {point} with numbers {numbers}, ratio: {numbers[0] * numbers[1]}")

    print(f"Gear sum: {gear_sum}")


if __name__ == "__main__":
    main()

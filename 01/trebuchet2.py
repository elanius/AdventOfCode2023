FILENAME = "input2.txt"

digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def find_digit(line, index):
    if line[index].isdigit():
        return int(line[index]), index + 1

    for digit, value in digits.items():
        if line.startswith(digit, index):
            return value, index + 1  # I need to parse also "oneight" as "one" and "eight

    return None, index + 1


def main():
    sum = 0

    # Read the input file
    with open(FILENAME) as f:
        lines = f.readlines()

    first_digit = None
    last_digit = None

    # Parse the input file
    for line in lines:
        index = 0
        line = line.rstrip()
        while index < len(line):
            digit, index = find_digit(line, index)
            if digit is None:
                continue
            if first_digit is None:
                first_digit = digit

            last_digit = digit

        print(f"Found number: {10 * first_digit + last_digit}, in line: {line}")

        sum += 10 * first_digit + last_digit
        first_digit = None
        last_digit = None

    print(f"Final sum from file: {FILENAME} is {sum}")


if __name__ == "__main__":
    main()

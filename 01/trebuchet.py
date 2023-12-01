FILENAME = "input.txt"
sum = 0


# Read the input file
with open(FILENAME) as f:
    lines = f.readlines()

first_digit = None
last_digit = None

# Parse the input file
for line in lines:
    for char in line:
        if char.isdigit():
            if first_digit is None:
                first_digit = int(char)

            last_digit = int(char)

    # print(f"First digit: {first_digit}, last digit: {last_digit} in file: {FILENAME}")

    sum += 10 * first_digit + last_digit
    first_digit = None
    last_digit = None

print(f"Final sum from file: {FILENAME} is {sum}")

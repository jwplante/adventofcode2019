
"""
James Plante
Advent of Code Day 4 Part 2 Implementation
"""

def isValidPassword(number):
    st_representation = str(number)
    last_digit = -1
    repeatDigit = False
    allIncreasing = True
    for digit in st_representation:
        current_digit = int(digit)
        if (last_digit == current_digit):
            repeatDigit = True
        if (last_digit > current_digit):
            allIncreasing = False
        last_digit = current_digit
    return repeatDigit and allIncreasing

counter = 0

for pw in range(130254, 678275):
    if (isValidPassword(pw)):
        counter += 1

print(counter)

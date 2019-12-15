"""
James Plante
Advent of Code Day 4 Part 2 Implementation
"""

def isValidPassword(number):
    st_representation = str(number)
    last_digit = -1
    allIncreasing = True
    frequencies = {"0" : 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0 , "6" : 0,
            "7" : 0, "8" : 0, "9" : 0}

    for digit in st_representation:
        current_digit = int(digit)

        frequencies[digit] += 1

        if (last_digit > current_digit):
            allIncreasing = False

        last_digit = current_digit

    return 2 in frequencies.values() and allIncreasing

counter = 0

for pw in range(130254, 678275):
    if (isValidPassword(pw)):
        counter += 1

print(counter)

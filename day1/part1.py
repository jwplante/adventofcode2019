
"""
Calculate the fuel based on the given mass
"""
def calculate_fuel(mass):
    return (mass // 3) - 2

f = open("input.txt", 'r')

total_fuel = 0

for number in f:
    total_fuel += calculate_fuel(int(number))

print(total_fuel)

f.close()

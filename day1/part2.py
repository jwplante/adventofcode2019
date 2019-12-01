
"""
Calculate the fuel based on the given mass
"""
def calculate_fuel(mass):
    total_for_mass = (mass // 3) - 2
    if (total_for_mass < 0):
        return 0
    else:
        total_for_mass += calculate_fuel(total_for_mass)
        return total_for_mass

f = open("input.txt", 'r')

total_fuel = 0

for number in f:
    total_fuel += calculate_fuel(int(number))

print(total_fuel)

f.close()

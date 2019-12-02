
"""
Given an array of integers, run the given program.
"""
def run_operation(array):

    size = len(array)
    pc = 0    # Program Counter
    exit_loop = False

    while (pc < size and not exit_loop):
        if (array[pc] == 1 and pc < size - 3):
            # Get inputs
            int_one = array[array[pc + 1]]
            int_two = array[array[pc + 2]]
            output_index = array[pc + 3]
            
            # Execute the command
            array[output_index] = int_one + int_two

            pc += 4
        elif (array[pc] == 2 and pc < size - 3):
            # Get inputs
            int_one = array[array[pc + 1]]
            int_two = array[array[pc + 2]]
            output_index = array[pc + 3]

            array[output_index] = int_one * int_two
            pc += 4
        elif (array[pc] == 99):
            exit_loop = True
        else:  ## Invalid opcode
            pc += 1

# Open and parse the file
with open("input.txt", 'r') as f:
    st_instructions = f.read()

# Convert to int array
instructions = list(map(int, st_instructions.split(',')))

run_operation(instructions)
print(instructions[0])

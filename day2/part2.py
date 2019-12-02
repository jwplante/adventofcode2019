
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
initial_instructions = list(map(int, st_instructions.split(',')))

for i in range(99):
    for j in range(99):
        new_instructions = initial_instructions.copy()
        new_instructions[1] = i
        new_instructions[2] = j
        run_operation(new_instructions)

        if (new_instructions[0] == 19690720):
            print("noun = " + str(i))
            print("verb = " + str(j))
            print("Final answer: " + str(100 * i + j))

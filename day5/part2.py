
class Computer:
    def __init__(self, prog):
        self.pc = 0         # Program Counter
        self.prog = prog    # Program Data
        self.debug = False  # Debug mode
        self.paused = False # Will take in new instructions but will not execute
        self.halted = False # Will stop the program

    def haltProgram(self):
        self.halted = True

    # Advance the program counter to a specific address
    def jumpTo(self, addr):
        self.pc = addr

    # Advance the PC by instructions
    def advanceProgCounter(self, instructions):
        self.pc += instructions

    # Gets the given modes for the opcode at PC
    def parseArguments(self):
        opcode = self.prog[self.pc] // 100
        ret_array = []
        for i in range(2):
            ret_array.append(opcode % 10)
            opcode //= 10
        if self.debug: print(ret_array)
        return ret_array
    
    # Gets the opcode number for the opcode at PC
    def getOpcode(self):
        return self.prog[self.pc] % 100

   # Stores the given value to the given address
    def storeConstant(self, addr, val):
        if (addr < len(self.prog)):
           self.prog[addr] = val
        else:
            print("Access out of bounds! Terminating program!")
            self.haltProgram()

    # Gives the correct value for the array access depending on the mode
    # @value - The true value (immediate) or address (position)
    def accessConstant(self, immediate, value):
        if (immediate == 1):
            return value
        elif (value < len(self.prog)):
            return self.prog[value]
        else:
            print("Access out of bounds! Terminating program!")
            self.haltProgram()

class IOSystem:
    def __init__(self, msg):
        self.msg = msg

    # Takes in the input from the user
    def getInput(self):
       return int(input(self.msg))

   # Puts the output to the terminal
    def putOutput(self, data):
       print(str(data)) 

# Controller to handle execution of all instructions
class InstructionSetController:
    def __init__(self, com, io):
        self.com = com # Main Computer instance
        self.io = io # IO class

    # Opcode 1
    # Takes 3 parameters
    # Adds together parameters 1 and 2 and stores in parameter 3's location
    def add(self):
        if (self.com.pc < len(self.com.prog) - 3):
            parameters = self.com.parseArguments()
            
            mode_param1 = parameters[0]
            mode_param2 = parameters[1]
            arg1 = self.com.accessConstant(mode_param1, self.com.prog[self.com.pc + 1])
            arg2 = self.com.accessConstant(mode_param2, self.com.prog[self.com.pc + 2])
            arg3 = self.com.prog[self.com.pc + 3]

            if self.com.debug: print("ADD(" + str(arg1) + ", " + str(arg2) + ") to " + str(arg3))
            self.com.storeConstant(arg3, arg1 + arg2)
            self.com.advanceProgCounter(4)
    
    # Opcode 2
    # Takes 3 parameters
    # Multiplies together parameters 1 and 2 and stores in parameter 3's location
    def multiply(self):
        if self.com.debug: print("MULTIPLY")
        if (self.com.pc < len(self.com.prog) - 3):
            parameters = self.com.parseArguments()

            mode_param1 = parameters[0]
            mode_param2 = parameters[1]
            arg1 = self.com.accessConstant(mode_param1, self.com.prog[self.com.pc + 1])
            arg2 = self.com.accessConstant(mode_param2, self.com.prog[self.com.pc + 2])
            arg3 = self.com.prog[self.com.pc + 3]

            if self.com.debug: print("MULT(" + str(arg1) + ", " + str(arg2) + ") to " + str(arg3))

            self.com.storeConstant(arg3, arg1 * arg2)
            self.com.advanceProgCounter(4)

    # Opcode 3
    # Takes 1 parameter
    # Stores the value of input into address parameter
    def inp(self):
        if self.com.debug: print("STORE")
        if (self.com.pc < len(self.com.prog) - 1):
            input = self.io.getInput()
            store_addr = self.com.accessConstant(0, self.com.pc + 1)
            self.com.storeConstant(store_addr, input)
            self.com.advanceProgCounter(2)
            if self.com.debug: print("STORE " + str(input) + " to " + str(store_addr))

    # Opcode 4
    # Takes 1 parameter
    # Takes the value of address parameter 1 and outputs it.
    def outp(self):
        if (self.com.pc < len(self.com.prog) - 1):
            parameters = self.com.parseArguments()
            val = -1
            if (parameters[0] == 1):
                val = self.com.prog[self.com.pc + 1]
            else:
                addr = self.com.prog[self.com.pc + 1]
                val = self.com.prog[addr]
            if self.com.debug: print("OUTPUT")
            self.io.putOutput(val)
            self.com.advanceProgCounter(2)

    # Opcode 5
    # Takes 2 parameters
    # If Param 1 is greater than 0, jump the PC to that value.
    def jumpIfTrue(self):
        if (self.com.pc < len(self.com.prog) - 2):
            parameters = self.com.parseArguments()
            mode_param1 = parameters[0]
            mode_param2 = parameters[1]
            arg1 = self.com.accessConstant(mode_param1, self.com.prog[self.com.pc + 1])
            arg2 = self.com.accessConstant(mode_param2, self.com.prog[self.com.pc + 2])

            if (arg1 > 0):
                self.com.jumpTo(arg2)
            else:
                self.com.advanceProgCounter(3)

    # Opcode 6
    # Takes 2 parameters
    # If Param 1 is equal to 0, jump the PC to that value.
    def jumpIfFalse(self):
        if (self.com.pc < len(self.com.prog) - 2):
            parameters = self.com.parseArguments()
            mode_param1 = parameters[0]
            mode_param2 = parameters[1]
            arg1 = self.com.accessConstant(mode_param1, self.com.prog[self.com.pc + 1])
            arg2 = self.com.accessConstant(mode_param2, self.com.prog[self.com.pc + 2])

            if (arg1 == 0):
                self.com.jumpTo(arg2)
            else:
                self.com.advanceProgCounter(3)

    # Opcode 7
    # Takes 3 Arguments
    # Stores 1 in address specified by parameter 3 if parameter 1 < parameter 2
    def lessThan(self):
        if (self.com.pc < len(self.com.prog) - 3):
            parameters = self.com.parseArguments()

            mode_param1 = parameters[0]
            mode_param2 = parameters[1]
            arg1 = self.com.accessConstant(mode_param1, self.com.prog[self.com.pc + 1])
            arg2 = self.com.accessConstant(mode_param2, self.com.prog[self.com.pc + 2])
            arg3 = self.com.prog[self.com.pc + 3]

            storeVal = 1 if (arg1 < arg2) else 0
            self.com.storeConstant(arg3, storeVal)

            self.com.advanceProgCounter(4)

    # Opcode 8
    # Takes 3 Arguments
    # Stores 1 in address specified by parameter 3 if parameter 1 == parameter 2
    def eq(self):
        if (self.com.pc < len(self.com.prog) - 3):
            parameters = self.com.parseArguments()

            mode_param1 = parameters[0]
            mode_param2 = parameters[1]
            arg1 = self.com.accessConstant(mode_param1, self.com.prog[self.com.pc + 1])
            arg2 = self.com.accessConstant(mode_param2, self.com.prog[self.com.pc + 2])
            arg3 = self.com.prog[self.com.pc + 3]

            storeVal = 1 if (arg1 == arg2) else 0
            self.com.storeConstant(arg3, storeVal)

            self.com.advanceProgCounter(4)

    # Opcode 99
    # Takes no arguments
    # Terminates the program
    def halt(self):
        if self.com.debug: print("HALT")
        self.com.haltProgram()
        self.com.advanceProgCounter(1)

    lookup_table = {1 : add,
                    2 : multiply,
                    3 : inp,
                    4 : outp,
                    5 : jumpIfTrue,
                    6 : jumpIfFalse,
                    7 : lessThan,
                    8 : eq,
                    99 : halt}

# Controller to handle the execution of the program
class ExecuteController:
    def __init__(self, com, io, inst_set):
        self.com = com # Main Computer instance
        self.io = io # IO class
        self.inst_set = inst_set # Instruction Set

    # Execute the program
    def executeProgram(self):
        while (self.com.pc < len(self.com.prog) and not self.com.halted):
            if self.com.debug: print("Current instruction: " + str(self.com.prog[self.com.pc]))
            if self.com.debug: print("Prog. Counter: " + str(self.com.pc))
            opcode = self.com.getOpcode()
            if self.com.debug: print("Current opcode: " + str(opcode))
            self.inst_set.lookup_table[opcode](self)


# Open and parse the file
with open("input.txt", 'r') as f:
    st_instructions = f.read()

# Convert to int array
initial_instructions = list(map(int, st_instructions.split(',')))

computer = Computer(initial_instructions)
io_system = IOSystem("Please enter Ship System ID: ")
inst_set = InstructionSetController(computer, io_system)
executor = ExecuteController(computer, io_system, inst_set)

executor.executeProgram()

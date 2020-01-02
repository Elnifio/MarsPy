import model
import sim_regs
import sim_mem
import baseConverter as cv


"""
Sample Programs. type in `python3 samples.py`, and follow the instruction provided. 
"""

__author__ = "Elnifio"


# Add the first five integers
def sum_unambiguous():
    memory = sim_mem.Memory()
    insts = {
        # main
        "0x00003000": "add $8, $0, $0",     # sum = 0
        "0x00003004": "add $9, $0, $0",     # for (i = 0; ...)
        # loop
        "0x00003008": "add $8, $8, $9",    # sum = sum + i
        "0x0000300C": "addi $9, $9, 1",     # for (...; ...; i++)
        "0x00003010": "slti $10, $9, 5",       # for (...; i<5) 
        "0x00003014": "bne $10, $0, -4",    # is $10 true? i.e., != 0
        # end
        "0x00003018": "ori $2, $0, 10",        # syscall 10 for exit
        "0x0000301C": "syscall"                     # we are out of here. 
    }

    model.run_instructions(insts, memory, ["$8", "$9", "$10"])


# Calculates the sum of an array
def sumArray():
    memory = sim_mem.Memory()
    memory.set_mem_by_word(0, "0x00000000") # Allocate space for sum, address at 0x0
    memory.set_mem_by_word(4, "0x00000000") # Allocate space for i, address at 0x4
    # Allocate space for a, address at 0x8
    a = [7, 8, 9, 10, 8]
    i = 2
    for item in a:
        memory.store_integer_at_address(i<<2, item)
        i += 1
    insts = {
        # main
        "0x00003000": "add $9, $0, $0", # i in $9 = 0
        "0x00003004": "add $8, $0, $0", # sum in $8 = 0
        # loop
        "0x00003008": "sll $10, $9, 2",     # convert i to word offset
        "0x0000300C": "lw $10, 8($10)", # load a[i]
        "0x00003010": "add $8, $8, $10",    # sum = sum + a[i]
        "0x00003014": "addi $9, $9, 1",     # for (...; ...; i++)
        "0x00003018": "slti $10, $9, 5",    # for (...; i<5; )
        "0x0000301C": "bne $10, $0, -6",   # loop back

        "0x00003020": "sw $8, 0($0)",   # update final sum in memory
        "0x00003024": "sw $9, 4($0)", # update final i in memory
        # end
        "0x00003028": "ori $2, $0, 10", # system call 10 for exit
        "0x0000302C": "syscall"     # we are out of here. 
    }
    print("Before Executing: Mem[8](sum): " + memory.get_mem_by_word(0))
    model.run_instructions(insts, memory, ["$8", "$9", "$10"])
    print("After Executing: Mem[8](sum): " + memory.get_mem_by_word(0))


# Calculates the largest Fibonacci number smaller than 100
def Fibonacci(): 
    memory = sim_mem.Memory()
    memory.set_mem_by_word(0, "0x00000000") # int x = 0; x = mem[0x0]
    memory.set_mem_by_word(4, "0x00000001") # int y = 0; y = mem[0x4]
    insts = {
        "0x00003000": "lw $8, 0($0)",
        "0x00003004": "lw $9, 4($0)",
        "0x00003008": "slti $10, $9, 100",
        "0x0000300C": "beq $10, $0, 4", 
        "0x00003010": "add $10, $0, $8",
        "0x00003014": "add $8, $0, $9",
        "0x00003018": "add $9, $10, $9", 
        "0x0000301C": "j 0x0C02",
        "0x00003020": "sw $8, 0($0)",
        "0x00003024": "sw $9, 4($0)",
        "0x00003028": "ori $2, $0, 10",
        "0x0000302C": "syscall"
    }
    print("Before Executing: Mem[0](x): " + memory.get_mem_by_word(0))
    model.run_instructions(insts, memory, ["$8", "$9", "$10"])
    print("After Executing: Mem[0](x): " + memory.get_mem_by_word(0))


# Calculates matrix multiplication. 
# Should first input matrix size (no larger than 10 * 10)
# And then enter numbers for Matrix A and Matrix B
# New matrix printed in the terminal.
def matrixMultiplication():
    memory = sim_mem.Memory()
    memory.allocate_space(0, 400)
    memory.allocate_space(400, 400)
    memory.allocate_space(800, 400)
    memory.store_char_at_address(1200, "\n")
    memory.store_char_at_address(1202, " ")
    insts = {
        # main
        # Reads m (matrix will be size m * m)
        "0x00003000": "addi $2, $0, 5",
        "0x00003004": "syscall",
        "0x00003008": "add $8, $0, $2",
        
        # for loop for reading matrix A
        "0x0000300C": "add $9, $0, $0",
        # for i in A:
        "0x00003010": "add $10, $0, $0",
        # for j in A[i]: 
        "0x00003014": "addi $2, $0, 5",
        "0x00003018": "syscall", 
        "0x0000301C": "mult $9, $8", 
        "0x00003020": "mflo $11",
        "0x00003024": "add $11, $11, $10",
        "0x00003028": "sll $11, $11, 2",
        "0x0000302C": "sw $2, 0($11)",
        "0x00003030": "addi $10, $10, 1",
        "0x00003034": "slt $11, $10, $8",
        "0x00003038": "bne $11, $0, -10",
        "0x0000303C": "addi $9, $9, 1", 
        "0x00003040": "slt $10, $9, $8",
        "0x00003044": "bne $10, $0, -14",

        # for loop for reading matrix B
        "0x00003048": "add $9, $0, $0",
        # for i in B:
        "0x0000304C": "add $10, $0, $0",
        # for j in B:
        "0x00003050": "addi $2, $0, 5",
        "0x00003054": "syscall",
        "0x00003058": "mult $9, $8",
        "0x0000305C": "mflo $11",
        "0x00003060": "add $11, $11, $10",
        "0x00003064": "sll $11, $11, 2",
        "0x00003068": "sw $2, 400($11)",
        "0x0000306C": "addi $10, $10, 1",
        "0x00003070": "slt $11, $10, $8", 
        "0x00003074": "bne $11, $0, -10",
        "0x00003078": "addi $9, $9, 1",
        "0x0000307C": "slt $10, $9, $8",
        "0x00003080": "bne $10, $0, -14",

        # for loop for calculating matrix C
        "0x00003084": "add $9, $0, $0",
        # for i in C:
        "0x00003088": "add $10, $0, $0",
        # for j in C:
        "0x0000308C": "add $15, $0, $0",
        "0x00003090": "add $12, $0, $0",
        # for index in range(m):
        "0x00003094": "mult $9, $8",
        "0x00003098": "mflo $11",
        "0x0000309C": "add $11, $11, $12",
        "0x000030A0": "sll $11, $11, 2",
        "0x000030A4": "lw $13, 0($11)",
        "0x000030A8": "mult $12, $8",
        "0x000030AC": "mflo $11",
        "0x000030B0": "add $11, $11, $10",
        "0x000030B4": "sll $11, $11, 2",
        "0x000030B8": "lw $14, 400($11)",
        "0x000030BC": "mult $13, $14",
        "0x000030C0": "mflo $13",
        "0x000030C4": "add $15, $15, $13",
        "0x000030C8": "addi $12, $12, 1",
        "0x000030CC": "slt $13, $12, $8",
        "0x000030D0": "bne $13, $0, -16",
        # END for index
        "0x000030D4": "mult $9, $8",
        "0x000030D8": "mflo $11",
        "0x000030DC": "add $11, $11, $10",
        "0x000030E0": "sll $11, $11, 2",
        "0x000030E4": "sw $15, 800($11)",
        "0x000030E8": "addi $10, $10, 1",
        "0x000030EC": "slt $11, $10, $8",
        "0x000030F0": "bne $11, $0, -26",
        # END for j in C
        "0x000030F4": "addi $9, $9, 1",
        "0x000030F8": "slt $10, $9, $8",
        "0x000030FC": "bne $10, $0, -30",
        # END for i in C

        # Prints the Result
        "0x00003100": "add $9, $0, $0",
        # for i in C:
        "0x00003104": "add $10, $0, $0",
        # for j in C:
        "0x00003108": "mult $9, $8", 
        "0x0000310C": "mflo $11",
        "0x00003110": "add $11, $11, $10",
        "0x00003114": "sll $11, $11, 2",
        "0x00003118": "lw $12, 800($11)",
        "0x0000311C": "addi $2, $0, 1",
        "0x00003120": "add $4, $0, $12",
        "0x00003124": "syscall",
        "0x00003128": "addi $2, $0, 4",
        "0x0000312C": "addi $4, $0, 1202", 
        "0x00003130": "syscall",
        "0x00003134": "addi $10, $10, 1",
        "0x00003138": "slt $11, $10, $8", 
        "0x0000313C": "bne $11, $0, -14",
        # END for j in C
        "0x00003140": "addi $2, $0, 4", 
        "0x00003144": "addi $4, $0, 1200", 
        "0x00003148": "syscall",
        "0x0000314C": "addi $9, $9, 1",
        "0x00003150": "slt $10, $9, $8", 
        "0x00003154": "bne $10, $0, -21",
        # END for i in C
        # EXIT:
        "0x00003158": "addi $2, $0, 10",
        "0x0000315C": "syscall"
    }
    model.run_instructions(insts, memory, {})


# prints all binary patterns of given length
# Should enter the length of binary patterns 
# Patterns printed in the terminal
def makePatterns():
    memory = sim_mem.Memory()
    memory.allocate_space(0, 84)
    memory.store_char_at_address(84, "\n")
    insts = {
        # MAIN
        "0x00003000": "ori $29, $0, 0x3000", 
        "0x00003004": "addi $30, $29, -4",
        "0x00003008": "addi $2, $0, 5",
        "0x0000300C": "syscall",
        "0x00003010": "add $8, $2, $0",
        "0x00003014": "addi $4, $8, 0",
        "0x00003018": "addi $5, $0, 0",
        "0x0000301C": "jal 0x00000C0A", # Jump to MakePatterns
        # END
        "0x00003020": "ori $2, $0, 10",
        "0x00003024": "syscall",
        # MakePatterns
        "0x00003028": "addi $29, $29, -8",
        "0x0000302C": "sw $31, 4($29)", 
        "0x00003030": "sw $30, 0($29)",
        "0x00003034": "addi $30, $29, 4",
        "0x00003038": "addi $29, $29, -4",
        "0x0000303C": "sw $4, 0($29)",
        "0x00003040": "addi $29, $29, -4",
        "0x00003044": "sw $5, 0($29)",
        "0x00003048": "slt $17, $5, $4",
        "0x0000304C": "addi $29, $29, -4",
        "0x00003050": "sw $17, 0($29)",
        "0x00003054": "beq $17, $0, 21", # beq PrintPatterns
        "0x00003058": "lw $17, -16($30)",
        "0x0000305C": "beq $17, $0, 15", # beq return
        "0x00003060": "sll $8, $5, 2",
        "0x00003064": "sw $0, 0($8)",
        "0x00003068": "lw $4, -8($30)",
        "0x0000306C": "lw $5, -12($30)",
        "0x00003070": "addi $5, $5, 1",
        "0x00003074": "jal 0x00000C0A", # Jump to MakePatterns
        "0x00003078": "lw $17, -16($30)", 
        "0x0000307C": "beq $17, $0, 7", # beq return
        "0x00003080": "lw $4, -8($30)", 
        "0x00003084": "lw $5, -12($30)",
        "0x00003088": "sll $8, $5, 2",
        "0x0000308C": "addi $9, $0, 1",
        "0x00003090": "sw $9, 0($8)",
        "0x00003094": "addi $5, $5, 1",
        "0x00003098": "jal 0x00000C0A",
        # RETURN
        "0x0000309C": "addi $29, $30, 4",
        "0x000030A0": "lw $31, 0($30)",
        "0x000030A4": "lw $30, -4($30)",
        "0x000030A8": "jr $31",
        # PrintPatterns
        "0x000030AC": "addi $29, $29, -8",
        "0x000030B0": "sw $31, 4($29)",
        "0x000030B4": "sw $30, 0($29)",
        "0x000030B8": "addi $30, $29, 4",
        "0x000030BC": "addi $17, $4, 0",
        "0x000030C0": "addi $8, $0, 0",
        # PrintWhile
        "0x000030C4": "beq $8, $17, 7", # beq PrintReturn
        "0x000030C8": "sll $9, $8, 2",
        "0x000030CC": "lw $10, 0($9)'",
        "0x000030D0": "addi $2, $0, 1",
        "0x000030D4": "add $4, $0, $10",
        "0x000030D8": "syscall",
        "0x000030DC": "addi $8, $8, 1",
        "0x000030E0": "j 0x00000C31", 
        # PrintReturn
        "0x000030E4": "addi $2, $0, 4",
        "0x000030E8": "addi $4, $0, 84", 
        "0x000030EC": "syscall",
        "0x000030F0": "addi $29, $30, 4",
        "0x000030F4": "lw $31, 0($30)",
        "0x000030F8": "lw $30, -4($30)",
        "0x000030FC": "jr $31",
    }
    model.run_instructions(insts, memory)


if __name__ == "__main__":
    print("Please select the demo program:")
    print("1. sum - sums the values in range(0, 5)")
    print("2. sumArray - sums values in [7, 8, 9, 10, 8]")
    print("3. Fibonacci - calculates the largest Fibonacci number lower than 100")
    print("4. Matrix Multiplication - calculates matrix multiplication (using loops)")
    print("5. Make Patterns - prints binary patterns of given length (using recursions)")
    option = input()
    if option == "1":
        sum_unambiguous()
    elif option == "2":
        sumArray()
    elif option == "3":
        Fibonacci()
    elif option == "4":
        matrixMultiplication()
    elif option == "5":
        makePatterns()
    else:
        print("Option not found. Have a nice day :)")
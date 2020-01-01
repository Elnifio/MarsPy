import sim_mem, model
def Fibonacci():
    memory = sim_mem.Memory()
    memory.store_integer_at_address(0x0, 0x0) # Allocate word for x, starting at address 0x0
    memory.store_integer_at_address(0x4, 0x1) # Allocate word for y, starting at address 0x4
    insts = {
        "0x00003000": "lw $8, 0x0($0)",
        "0x00003004": "lw $9, 0x4($0)",
        "0x00003008": "slti $10, $9, 100",
        "0x0000300C": "beq $10, $0, 4",
        "0x00003010": "add $10, $0, $8",
        "0x00003014": "add $8, $0, $9",
        "0x00003018": "add $9, $10, $9",
        "0x0000301C": "j 0x00000C02",
        "0x00003020": "sw $8, 0x0($0)",
        "0x00003024": "sw $9, 0x4($0)",
        "0x00003028": "ori $2, $0, 10",
        "0x0000302C": "syscall",
    }
    
    model.run_instructions(insts, memory, [])


if __name__ == "__main__":
    Fibonacci()
import sim_mem, model
def sumArray():
    memory = sim_mem.Memory()
    memory.allocate_space(0x0, 0x4) # 4 space allocated for sum, starting at 0x0
    memory.allocate_space(0x4, 0x4) # 4 space allocated for i, starting at 0x4
    # Allocate Words for a, starting at address 0x8
    a = [0x00000007, 0x00000008, 0x00000009, 0x0000000A, 0x00000008]
    current_address = 8
    for x in a:
        memory.store_integer_at_address(current_address, x)
        current_address += 4
    insts = {
        "0x00003000": "add $9, $0, $0",
        "0x00003004": "add $8, $0, $0",
        "0x00003008": "sll $10, $9, 2",
        "0x0000300C": "lw $10, 0x8($10)",
        "0x00003010": "add $8, $8, $10",
        "0x00003014": "addi $9, $9, 1",
        "0x00003018": "slti $10, $9, 5",
        "0x0000301C": "bne $10, $0, -6",
        "0x00003020": "sw $8, 0x0($0)",
        "0x00003024": "sw $9, 0x4($0)",
        "0x00003028": "ori $2, $0, 10",
        "0x0000302C": "syscall",
    }
    
    model.run_instructions(insts, memory, [])


if __name__ == "__main__":
    sumArray()
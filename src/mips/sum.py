import sim_mem, model
def sum():
    memory = sim_mem.Memory()
    insts = {
        "0x00003000": "add $8, $0, $0",
        "0x00003004": "add $9, $0, $0",
        "0x00003008": "add $8, $8, $9",
        "0x0000300C": "addi $9, $9, 1",
        "0x00003010": "slti $10, $9, 5",
        "0x00003014": "bne $10, $0, -4",
        "0x00003018": "ori $2, $0, 10",
        "0x0000301C": "syscall",
    }
    
    model.run_instructions(insts, memory, [])


if __name__ == "__main__":
    sum()
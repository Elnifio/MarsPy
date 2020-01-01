import controller
import sim_regs
import sim_mem
import Termination

__author__ = "Elnifio"

def run_instructions(insts, memory, registers_to_print={}, step_by_step=False, debug=False):
    MAX = 10000
    registers = sim_regs.Register()
    
    if not "PC" in registers: 
        raise ValueError("PC not in registers, please check your configurations.")
    counter = 0
    if not len(registers_to_print) == 0: 
        print({x: registers[x] for x in registers_to_print})
    while (registers["PC"] in insts):
        try:
            if step_by_step:
                input("executing " + insts[registers["PC"]] + ".")
            controller.control(insts[registers["PC"]], memory, registers)
            counter += 1
        except Termination.Termination as t:
            print("-------- Program Finished Running. --------")
            break
        except ValueError as e:
            print("ValueError at " + registers["PC"] + ": " + str(e) + "")
            if debug:
                print("Current Registers: ")
                print(registers.getRegs())
            break
        if counter >= MAX:
            raise ValueError("There might be a possible infinite loop, please check your code or modify the MAX value. ")
    if not len(registers_to_print) == 0: 
        print({x: registers[x] for x in registers_to_print})
    
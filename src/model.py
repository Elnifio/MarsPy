import controller
import sim_regs
import sim_mem
import Termination


"""
This module contains only one method which runs the instructions.
"""


__author__ = "Elnifio"


# Runs the instructions passed in. 
# @Params: 
#                   insts: Instruction dictionary. Each elements is a Program_address - Instruction pair. 
#                           For more instruction samples, view samples.py
#                   memory: a sim_mem.Memory object. 
#                   registers_to_print: an iterable object that contains all registers that needs to be printed. This could be used to check if your program functions normally. 
#                           For instance, if you wish to print $8 - $10, you could pass in ["$8", "$9", "$10"] or ["$" + str(x) for x in range(8, 11)]
#                   step_by_step: a boolean value indicating if this program should be executed step-by-step. 
#                           In step-by-step mode, for each instructions, the console will prompt the instruction that it needs to be executed, and then you need to press "Enter" or "Return" on your keyboard to proceed.
#                   debug: a boolean value indicating if you need to debug. 
#                           In debug mode, when an error is encountered, the program will print out all register values. 
# Return: None.
# Raise: None. 
# Notice the MAX property which counts the number of instructions used. If MAX is reached, the program will stop and ask if you have encountered an infinite loop. 
#                   If you believe that your program cannot create an infinite loop, you could modify this value here. 
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
    
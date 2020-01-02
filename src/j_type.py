import database as db
import baseConverter as cv
import functools


"""
This module defines J-type instruction behaviors. 
For all methods below (only two methods):
        Explanation for Parameter lists: 
            cmd_list represents an array containing separated parts of the instruction. For instance, 
                    "addi $8, $9, 12" -> ["addi", "$8", "$9", "12"]
                    "lw $8, 0x04($12)" -> ["lw", "$8", "0x04($12)"]
                    "mult $8, $9" -> ["mult", "$8", "$9"]
            sim_regs represents a sim_regs.Register object
        None of these methods have return value. 
        All methods name and functionality corresponds to theirselves in database module.
        All instruction format corresponds to MIPS instruction format. i.e., for "addi $8, $9, 10", it is expected that cmd_list[1] and cmd_list[2] should be registers and cmd_list[3] should be a number.
        All methods raises these errors:
            ValueError if immediate cannot be recognized.
            ValueError if operands missing.
            ValueError if registers cannot be recognized or PC not in registers. 
"""


__author__ = "Elnifio"


def jump(cmd_list, sim_regs):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    address = cmd_list[1]
    if "0x" in address:
        address = int(address, 16)
    elif "0b" in address: 
        address = int(address, 2)
    else:
        try:
            address = int(address)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate")
    if not len(cmd_list) == 2:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"") 
    if not "PC" in sim_regs:
        raise ValueError("PC not in simulated Registers, please check your configuration.")
    sim_regs["PC"] = cv.dec_to_hex(db.jump(cv.hex_to_dec(sim_regs["PC"]), address))


def jal(cmd_list, sim_regs):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    address = cmd_list[1]
    if "0x" in address:
        address = int(address, 16)
    elif "0b" in address: 
        address = int(address, 2)
    else:
        try:
            address = int(address)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate")
    if not len(cmd_list) == 2:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"") 
    if not ("PC" in sim_regs and ("$31" in sim_regs or "$ra" in sim_regs)):
        raise ValueError("PC or $ra not in simulated Registers, please check your configuration.")
    ra_name = "$31"
    if not ra_name in sim_regs:
        ra_name = "$ra"
    pc, ra = db.jal(cv.hex_to_dec(sim_regs["PC"]), address)
    sim_regs["PC"] = cv.dec_to_hex(pc)
    sim_regs[ra_name] = cv.dec_to_hex(ra)

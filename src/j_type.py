import database as db
import baseConverter as cv
import functools

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

import database as db
import functools
import baseConverter as cv
import re

"""
This module defines I-type instruction behaviors. 
For all methods below:
        Explanation for Parameter lists: 
            cmd_list represents an array containing separated parts of the instruction. For instance, 
                    "addi $8, $9, 12" -> ["addi", "$8", "$9", "12"]
                    "lw $8, 0x04($12)" -> ["lw", "$8", "0x04($12)"]
                    "mult $8, $9" -> ["mult", "$8", "$9"]
            sim_regs represents a sim_regs.Register object
            sim_mem represents a sim_mem.Memory object
        None of these methods have return value. 
        All methods name and functionality corresponds to theirselves in database module.
        All instruction format corresponds to MIPS instruction format. i.e., for "addi $8, $9, 10", it is expected that cmd_list[1] and cmd_list[2] should be registers and cmd_list[3] should be a number.
        All methods raises these errors:
            ValueError if immediate cannot be recognized.
            ValueError if operands missing.
            ValueError if registers cannot be recognized. 
            Any other Errors that original functions from database raise. 
"""

__author__ = "Elnifio"


def addi(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    imm = cmd_list[3]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.addi(rs, imm))


def addiu(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    imm = cmd_list[3]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.addiu(rs, imm))


def andi(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    imm = cmd_list[3]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.andi(rs, imm))


def beq(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    offset = cmd_list[3]
    if "0x" in offset:
        offset = int(offset, 16)
    elif "0b" in offset:
        offset = int(offset, 2)
    else:
        try:
            offset = int(offset)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and ("PC" in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[1]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[2]])
    pc = cv.hex_to_dec(sim_regs["PC"])
    sim_regs["PC"] = cv.dec_to_hex(pc + db.beq(rs, rt, offset))


def bne(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    offset = cmd_list[3]
    if "0x" in offset:
        offset = int(offset, 16)
    elif "0b" in offset:
        offset = int(offset, 2)
    else:
        try:
            offset = int(offset)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and ("PC" in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[1]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[2]])
    pc = cv.hex_to_dec(sim_regs["PC"])
    sim_regs["PC"] = cv.dec_to_hex(pc + db.bne(rs, rt, offset))


def lui(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    imm = cmd_list[2]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    if not len(cmd_list) == 3: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.lui(imm))


def lb(cmd_list, sim_regs, sim_mems):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 3:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = cmd_list[2]
    if not ("(" in mem_location and ")" in mem_location):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = re.split(r'[()]+', mem_location)
    imm = mem_location[0]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    rs = cv.hex_to_dec(sim_regs[mem_location[1]])
    sim_regs[cmd_list[1]] = db.lb(rs, imm, sim_mems)


def sb(cmd_list, sim_regs, sim_mems):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 3:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = cmd_list[2]
    if not ("(" in mem_location and ")" in mem_location):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = re.split(r'[()]+', mem_location)
    imm = mem_location[0]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    rs = cv.hex_to_dec(sim_regs[mem_location[1]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[1]])
    db.sb(rt, rs, imm, sim_mems)


def lw(cmd_list, sim_regs, sim_mems):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 3:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = cmd_list[2]
    if not ("(" in mem_location and ")" in mem_location):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = re.split(r'[()]+', mem_location)
    imm = mem_location[0]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    rs = cv.hex_to_dec(sim_regs[mem_location[1]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.lw(rs, imm, sim_mems))


def sw(cmd_list, sim_regs, sim_mems):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 3:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = cmd_list[2]
    if not ("(" in mem_location and ")" in mem_location):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    mem_location = re.split(r'[()]+', mem_location)
    imm = mem_location[0]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    rs = cv.hex_to_dec(sim_regs[mem_location[1]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[1]])
    db.sw(rt, rs, imm, sim_mems)


def ori(cmd_list, sim_regs):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs and cmd_list[2] in sim_regs):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    imm = cmd_list[3]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.ori(rs, imm))


def slti(cmd_list, sim_regs):
    instruction_literal = functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4:
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs and cmd_list[2] in sim_regs):
        raise ValueError("Illegal Operand at \"" + instruction_literal + "\"")
    imm = cmd_list[3]
    if "0x" in imm:
        imm = int(imm, 16)
    elif "0b" in imm:
        imm = int(imm, 2)
    else:
        try:
            imm = int(imm)
        except ValueError as e:
            raise ValueError("Unrecognizable Immediate.")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.slti(rs, imm))
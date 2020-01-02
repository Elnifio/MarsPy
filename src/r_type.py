import database as db
import functools
import baseConverter as cv


"""
This module defines R-type instruction behaviors. 
For all methods below:
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
            ValueError if immediate (shamt) cannot be recognized. This applies to Shift operations. 
            ValueError if operands missing.
            ValueError if registers cannot be recognized. 
            Any other Errors that original functions from database raise. 
"""


__author__ = "Elnifio"


def add(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (cmd_list[3] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[3]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.add(rs, rt))
    

def addu(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (cmd_list[3] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[3]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.addu(rs, rt))


def and_unambiguous(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (cmd_list[3] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[3]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.and_unambiguous(rs, rt))


def jr(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 2: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs and "PC"  in sim_regs):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    sim_regs["PC"] = sim_regs[cmd_list[1]]


def mult(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 3: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs and cmd_list[2]  in sim_regs):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[1]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs["hi"], sim_regs["lo"] = db.mult(rs, rt)
    sim_regs["hi"] = cv.dec_to_hex(sim_regs["hi"])
    sim_regs["lo"] = cv.dec_to_hex(sim_regs["lo"])


def mfhi(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 2: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs and "hi" in sim_regs):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    sim_regs[cmd_list[1]] = sim_regs["hi"]


def mflo(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 2: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not (cmd_list[1] in sim_regs and "lo" in sim_regs):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    sim_regs[cmd_list[1]] = sim_regs["lo"]


def nor(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (cmd_list[3] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[3]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.nor(rs, rt))


def or_unambiguous(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (cmd_list[3] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[3]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.or_unambiguous(rs, rt))


def slt(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (cmd_list[3] in sim_regs)):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rs = cv.hex_to_dec(sim_regs[cmd_list[2]])
    rt = cv.hex_to_dec(sim_regs[cmd_list[3]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.slt(rs, rt))


def sll(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    shamt = cmd_list[3]
    if shamt[:2] == "0x":
        shamt = int(shamt, 16)
    elif shamt[:2] == "0b":
        shamt = int(shamt, 2)
    else:
        shamt = int(shamt)
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (shamt in range(32))):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rt = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.sll(rt, shamt))


def srl(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    shamt = cmd_list[3]
    if shamt[:2] == "0x":
        shamt = int(shamt, 16)
    elif shamt[:2] == "0b":
        shamt = int(shamt, 2)
    else:
        shamt = int(shamt)
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (shamt in range(32))):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rt = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.srl(rt, shamt))


def sra(cmd_list, sim_regs):
    instruction_literal =  functools.reduce(lambda x, y: x + " " + y, cmd_list)
    if not len(cmd_list) == 4: 
        raise ValueError("Missing Operands for instruction \"" + instruction_literal + "\"")
    shamt = cmd_list[3]
    if shamt[:2] == "0x":
        shamt = int(shamt, 16)
    elif shamt[:2] == "0b":
        shamt = int(shamt, 2)
    else:
        shamt = int(shamt)
    if not ((cmd_list[1] in sim_regs) and (cmd_list[2] in sim_regs) and (shamt in range(32))):
        raise ValueError("Illegal Operand at \"" +  instruction_literal + "\"")
    rt = cv.hex_to_dec(sim_regs[cmd_list[2]])
    sim_regs[cmd_list[1]] = cv.dec_to_hex(db.sra(rt, shamt))
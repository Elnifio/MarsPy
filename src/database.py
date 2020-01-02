from datetime import datetime
from baseConverter import *
import functools
import re

"""
This module defines all behaviors of a MIPS Control Unit.
"""

__author__ = "Elnifio"

# Helper Functions
int16 = functools.partial(int, base=16)


# Add instruction. Returns a decimal value. 
# rd = add(rs + rt)
# @Params: rs, rt: integers
# Returns: rd: integer
# Raises: ValueError for overflow. 
def add(rs, rt):
    result = bin_to_dec(dec_to_bin(rs + rt))
    if result != (rs + rt):
        raise ValueError("Overflow caused by " + str(rs) + " + " + str(rt) + ".")
    return result

# Add unsigned instruction. Returns a decimal value.
# rd = addu(rs, rt)
# @Params: rs, rt: integers
# Returns: rd: integer
def addu(rs, rt):
    return bin_to_dec(dec_to_bin(rs + rt))

# Add immediate instruction. Returns a decimal value.
# Notice that you should not directly pass in an integer larger than 0x0000FFFF since extra bits will be stripped to perform sign extension
# rt = addi(rs, immediate)
# @Params: rs, imm: integers
# Returns: rt: integer
# Raises: ValueError for overflow
def addi(rs, imm):
    imm = dec_to_bin(imm, 16)
    sgn_ext = functools.reduce(lambda x, y: str(x) + str(y), [imm[0] for x in range(16)])
    imm = bin_to_dec(sgn_ext + imm)
    result = bin_to_dec(dec_to_bin(rs + imm))
    if result != (rs + imm):
        raise ValueError("Overflow caused by " + str(rs) + " + " + str(imm) + ".")
    return result

# Add immediate unsigned instruction. Returns a decimal value.
# rt = addiu(rs, immediate) 
# @Params: rs, imm: integers
# Returns: rt: integer
def addiu(rs, imm):
    imm = dec_to_bin(imm, 16)
    sgn_ext = functools.reduce(lambda x, y: str(x) + str(y), [imm[0] for x in range(16)])
    imm = bin_to_dec(sgn_ext + imm)
    return bin_to_dec(dec_to_bin(rs + imm))

# And instruction. Please do not directly type `and(rs, rt)`. 
# rd = and_unambiguous(rs, rt) 
# @Params: rs, rt: integers
# Returns: rd: integer
def and_unambiguous(rs, rt):
    return rs & rt

# And immediate instruction. Returns a decimal value. 
# Same notice for add immediate. immediates are expected to be no larger than 0x0000FFFF
# rt = andi(rs, immediate) 
# @Params: rs, imm: integers
# Returns: rt: integer
def andi(rs, imm):
    immediate = dec_to_bin(imm)
    immediate = bin_to_dec("0000000000000000" + immediate[16:])
    return rs & immediate

# Branch on equal instruction. Returns a decimal offset.
# Normally we do not expect offset to be larger than 1000. If you insist on doing this, please be aware of potential issues. 
# PC = PC + beq(rs, rt, offset) 
# @Params: rs, rt, offset: integers
# Return: difference between the new and old Program Counters. If you wish to use this instruction, please assign the program counter to (itself + return value of beq)
def beq(rs, rt, offset):
    if (rs == rt):
        return 4 + 4 * offset
    else:
        return 4 

# Same as beq. 
# PC = PC + bne(rs, rt, offset) 
def bne(rs, rt, offset):
    if (rs != rt):
        return 4 + 4 * offset
    else:
        return 4

# Jump instruction. Returns the destination address in unsigned decimal. 
# PC = jump(PC, addr) 
# @Params: pc, addr: unsigned integers
# Return: new_address: unsigned integer
def jump(pc, addr):
    return bin_to_dec_unsigned(dec_to_bin(pc)[:4] + dec_to_bin(addr * 4)[4:])

# Jump and Link instruction. Returns the jump address and PC + 4 in unsigned decimal
# PC, ra = jal(PC, addr) 
# @Params: pc, addr: unsigned integers
# Returns: PC, ra: unsigned integers. If you wish to use this instruction, please be aware that it has two return values.
def jal(pc, addr):
    ra = pc + 4
    return jump(pc, addr), ra

# Jump Register instruction. Returns the jump address. 
# PC = jr(rs)
# @Params: rs: integer
# Return: PC: integer
def jr(rs):
    return rs

# Load Upper Immediate instruction. Returns a decimal value
# Same notice for addi. immediates are not expected to be larger than 0x0000FFFF.
# rt = lui(imm) 
# @Param: imm: integer
# Return: rt: integer. 
def lui(imm):
    return bin_to_dec(dec_to_bin(imm)[16:] + "0000000000000000")

# Load word instruction. Returns the value at destinated address. 
# rt = Mem[rs + imm]
# @Params:
#                   rs, imm: integers
#                   sim_mem: a sim_mem.Memory object
# Return: rt: a decimal integer stored in particular location in memory.
# Raises: Please check get_mem_by_word method in sim_mem module.
def lw(rs, imm, sim_mem):
    address = rs + imm
    return bin_to_dec(hex_to_bin(sim_mem.get_mem_by_word(address)))

# Store word instruction. Returns nothing.
# Same notice for addi. immediates are not expected to be larger than 0x0000FFFF.
# Mem[rs + imm] = rt
# @Params:
#                   rt, rs, imm: integers, Notice that all of them are decimal integers! Please do not pass in hex strings and binary strings directly.
#                   sim_mem: sim_mem.Memory object
# Return: Nothing since it directly modifies contents in sim_mem.Memory object
# Raises: Please check set_mem_by_word method in sim_mem module.
def sw(rt, rs, imm, sim_mem):
    address = rs + imm
    sim_mem.set_mem_by_word(address, bin_to_hex(dec_to_bin(rt)))

# Load Byte Instruction. Returns the value at destinated address. 
# rt = Mem[rs + imm] (Hexadecimal, Only two bits, extra bits zero-padded)
# @Params: 
#                   rs, imm: integers.
#                   sim_mem: sim_mem.Memory object
# Return: rt: a **HEXADECIMAL** string stored in particular location in memory. Extra bits zero-padded. 
# Raises: Please check get_mem_by_byte method in sim_mem module.
def lb(rs, imm, sim_mem):
    address = rs + imm
    return sim_mem.get_mem_by_byte(address)

# Store Byte Instruction. Returns Nothing.
# Mem[rs + imm] = rt<7:0> (Hexadecimal)
# @Params: 
#                   rs, rt, imm: integers.
#                   sim_mem: sim_mem.Memory object
# Return: Nothing
# Raises: Please check set_mem_by_byte method in sim_mem module.
def sb(rt, rs, imm, sim_mem):
    address = rs + imm
    sim_mem.set_mem_by_byte(address, dec_to_hex(rt))

# Nor instruction.
# rd = nor(rs, rt)
# @Params: rs, rt: integers
# Return: rd: integer
def nor(rs, rt):
    return ~(rs | rt)

# Or instruction. Please do not directly type `or(rs, rt)`
# rd = or_unambiguous(rs, rt) 
# @Params: rs, rt: integers
# Return: rd: integer
def or_unambiguous(rs, rt):
    return rs | rt

# Or immediate instruction. Immediate zero-padded
# rt = ori(rs, ZeroExtImm)
# @Params: rs, imm: integers
# Return: rt: integer
def ori(rs, imm):
    immediate = "0000000000000000" + dec_to_bin(imm)[16:]
    return rs | bin_to_dec(immediate)

# Set less than instruction.
# rd = (rs < rt) ? 1 : 0
# @Params: rs, rt: integers
# Return: rd: integer (either 0 or 1)
def slt(rs, rt):
    if (rs < rt):
        return 1
    else:
        return 0

# Set less than immediate instruction. Literally the same as slt instruction. 
# rt = (rs < imm) ? 1 : 0
def slti(rs, imm):
    if (rs < imm):
        return 1
    else:
        return 0

# Shift Left Logical Instruction. Returns an integer.
# rd = sll(rt, shamt)
# @Params: rt, shamt: integers
# Returns: rd: integer
def sll(rt, shamt):
    return bin_to_dec(dec_to_bin(rt << shamt))

# Shift Right Logical Instruction. Returns an integer.
# rd = srl(rt, shamt)
# @Params: rt, shamt: integers
# Return: rd: integer
def srl(rt, shamt):
    zero_string = functools.reduce(lambda x, y: str(x) + str(y), ["0" for x in range(shamt)]) # Cannot use >> since python does not support Shift Right Logical Operation.
    return bin_to_dec((zero_string + dec_to_bin(rt))[:32])

# Shift Right Arithmetic Instruction. Returns an integer.
# rd = sra(rt, shamt)
# @Params: rt, shamt: integers
# Returns: rd: integer
def sra(rt, shamt):
    return bin_to_dec(dec_to_bin(rt >> shamt))

# Multiply instruction. Notice that there are two return values if you wish to use this method. 
# hi, lo = mult(rs, rt) 
# @Params: rs, rt: integers
# Return: hi, lo: integers
def mult(rs, rt):
    result = dec_to_bin(rs * rt, 64) 
    hi = result[:32]
    lo = result[32:]
    return bin_to_dec(hi), bin_to_dec(lo)

# Move From High instruction. 
# rd = mfhi(hi)
# @Param: hi: integer
# Return: rd: integer
def mfhi(hi):
    return hi

# Move From Low Instruction. 
# rd = mflo(lo) 
# @Param: lo: integer
# Return: rd: integer
def mflo(lo):
    return lo

# Exclusive or instruction. 
# rd = xor(rs, rt)
# @Params: rs, rt: integers
# Return: rd: integer
def xor(rs, rt):
    return rs ^ rt

# Exclusive Or Immediate Instruction. 
# rt = xori(rs, imm)
# @Params: rs, imm: integers
# Return: rt: integer
def xori(rs, imm):
    immediate = bin_to_dec("0000000000000000" + dec_to_bin(imm, 16)) 
    return rs ^ immediate

# CONFIG
R_TYPE = {
    "add": {"OP": 0x00, "FN": 0x20, "Function": add}, 
    "addu": {"OP": 0x00, "FN": 0x21, "Function": addu},
    "and": {"OP": 0x00, "FN": 0x24, "Function": and_unambiguous},
    "jr": {"OP": 0x00, "FN": 0x08, "Function": jr},
    "mult": {"OP": 0x00, "FN": 0x18, "Function": mult},
    "mfhi": {"OP": 0x00, "FN": 0x10, "Function": mfhi},
    "mflo": {"OP": 0x00, "FN": 0x12, "Function": mflo},
    "nor": {"OP": 0x0, "FN": 0x27, "Function": nor},
    "or": {"OP": 0x0, "FN": 0x25, "Function": or_unambiguous},
    "slt": {"OP": 0x0, "FN": 0x2a, "Function": slt},
    "sll": {"OP": 0x0, "FN": 0x00, "Function": sll},
    "srl": {"OP": 0x0, "FN": 0x02, "Function": srl},
    "sra": {"OP": 0x0, "FN": 0x03, "Function": sra},
}

I_TYPE = {
    "addi": {"OP": 0x08, "Function": addi},
    "addiu": {"OP": 0x09, "Function": addiu},   
    "andi": {"OP": 0xC, "Function": andi},
    "beq": {"OP": 0x4, "Function": beq},
    "bne": {"OP": 0x5, "Function": bne},
    "lui": {"OP": 0x0F, "Function": lui},
    "lb": {"OP": 0x20, "Function": lb},
    "lw": {"OP": 0x23, "Function": lw},
    "ori": {"OP": 0x0d, "Function": ori},
    "slti": {"OP": 0x0a, "Function": slti},
    "sb": {"OP": 0x28, "Function": sb},
    "sw": {"OP": 0x2b, "Function": sw},
}

J_TYPE = {
    "j": {"OP": 0x02, "Function": jump},
    "jal": {"OP": 0x03, "Function": jal}
}

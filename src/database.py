from datetime import datetime
from baseConverter import *
import functools
import re

__author__ = "Elnifio"

# Functions
int16 = functools.partial(int, base=16)


# rd = add(rs + rt) (decimal)
def add(rs, rt):
    result = bin_to_dec(dec_to_bin(rs + rt))
    if result != (rs + rt):
        raise ValueError("Overflow caused by " + str(rs) + " + " + str(rt) + ".")
    return result

# rd = addu(rs, rt) (decimal)
def addu(rs, rt):
    return bin_to_dec(dec_to_bin(rs + rt))

# rt = addi(rs, immediate) (decimal)
def addi(rs, imm):
    imm = dec_to_bin(imm, 16)
    sgn_ext = functools.reduce(lambda x, y: str(x) + str(y), [imm[0] for x in range(16)])
    imm = bin_to_dec(sgn_ext + imm)
    result = bin_to_dec(dec_to_bin(rs + imm))
    if result != (rs + imm):
        raise ValueError("Overflow caused by " + str(rs) + " + " + str(imm) + ".")
    return result

# rt = addiu(rs, immediate) (decimal)
def addiu(rs, imm):
    imm = dec_to_bin(imm, 16)
    sgn_ext = functools.reduce(lambda x, y: str(x) + str(y), [imm[0] for x in range(16)])
    imm = bin_to_dec(sgn_ext + imm)
    return bin_to_dec(dec_to_bin(rs + imm))

# rd = and_unambiguous(rs, rt) (decimal)
def and_unambiguous(rs, rt):
    return rs & rt

# rt = andi(rs, immediate) (decimal)
def andi(rs, imm):
    immediate = dec_to_bin(imm)
    immediate = bin_to_dec("0000000000000000" + immediate[16:])
    return rs & immediate

# PC = PC + beq(rs, rt, offset) (decimal)
def beq(rs, rt, offset):
    if (rs == rt):
        return 4 + 4 * offset
    else:
        return 4 

# PC = PC + bne(rs, rt, offset) (decimal)
def bne(rs, rt, offset):
    if (rs != rt):
        return 4 + 4 * offset
    else:
        return 4

# PC = jump(PC, addr) (decimal, unsigned)
def jump(pc, addr):
    return bin_to_dec_unsigned(dec_to_bin(pc)[:4] + dec_to_bin(addr * 4)[4:])

# PC, ra = jal(PC, addr) (decimal, unsigned)
def jal(pc, addr):
    ra = pc + 4
    return jump(pc, addr), ra

# PC = jr(rs) (decimal)
def jr(rs):
    return rs

# rt = lui(imm) (decimal)
def lui(imm):
    return bin_to_dec(dec_to_bin(imm)[16:] + "0000000000000000")

# rt = Mem[rs + imm] (decimal)
def lw(rs, imm, sim_mem):
    address = rs + imm
    return bin_to_dec(hex_to_bin(sim_mem.get_mem_by_word(address)))

# Mem[rs + imm] = rt (decimal)
def sw(rt, rs, imm, sim_mem):
    address = rs + imm
    sim_mem.set_mem_by_word(address, bin_to_hex(dec_to_bin(rt)))

# rt = Mem[rs + imm] (Hexadecimal, Only two bits, extra bits zero-padded)
def lb(rs, imm, sim_mem):
    address = rs + imm
    return sim_mem.get_mem_by_byte(address)

# Mem[rs + imm] = rt<7:0> (Hexadecimal)
def sb(rt, rs, imm, sim_mem):
    address = rs + imm
    sim_mem.set_mem_by_byte(address, dec_to_hex(rt))

# rd = nor(rs, rt) (decimal)
def nor(rs, rt):
    return ~(rs | rt)

# rd = or_unambiguous(rs, rt) (decimal)
def or_unambiguous(rs, rt):
    return rs | rt

# rt = ori(rs, ZeroExtImm) (decimal)
def ori(rs, imm):
    immediate = "0000000000000000" + dec_to_bin(imm)[16:]
    return rs | bin_to_dec(immediate)

# rd = (rs < rt) ? 1 : 0
def slt(rs, rt):
    if (rs < rt):
        return 1
    else:
        return 0

# rt = (rs < imm) ? 1 : 0
def slti(rs, imm):
    if (rs < imm):
        return 1
    else:
        return 0

# rd = sll(rt, shamt) (decimal)
def sll(rt, shamt):
    return bin_to_dec(dec_to_bin(rt << shamt))

# rd = srl(rt, shamt) (decimal)
def srl(rt, shamt):
    zero_string = functools.reduce(lambda x, y: str(x) + str(y), ["0" for x in range(shamt)])
    return bin_to_dec((zero_string + dec_to_bin(rt))[:32])

# rd = sra(rt, shamt) (decimal)
def sra(rt, shamt):
    return bin_to_dec(dec_to_bin(rt >> shamt))

# hi, lo = mult(rs, rt) (decimal)
def mult(rs, rt):
    result = dec_to_bin(rs * rt, 64) 
    hi = result[:32]
    lo = result[32:]
    return bin_to_dec(hi), bin_to_dec(lo)

# rd = mfhi(hi) (decimal)
def mfhi(hi):
    return hi

# rd = mflo(lo) (decimal)
def mflo(lo):
    return lo

# rd = xor(rs, rt) (decimal)
def xor(rs, rt):
    return rs ^ rt

# 
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

def test():
    t0 = int16("0x56781234")
    print(bin_to_hex(dec_to_bin(xori(t0, -12))))

def testMemory():
    mem = ["0x6C6C6568", "0x0000006F", "0x00000001", "0x101023F"]
    t0 = 3
    t0 = t0 << 2
    t0 = lw(0, 0x0, mem)
    print(mem)
    print(t0)
    print(hex(t0))
    print(bin_to_hex(dec_to_bin(t0)))
    t0 = lui(int16("0x00005678"))
    sw(t0, 0, 0xC, mem)
    print(mem)
    t0 = lb(0, 0, mem)
    print(t0)
    t0 = int16("0x5678ABCD")
    sb(t0, 0, 7, mem)
    print(mem)
    
def testBTH():
    a = "0x5678ABCD"
    print(a)
    print(bin_to_hex(hex_to_bin(a)))



if __name__ == "__main__":
    test()
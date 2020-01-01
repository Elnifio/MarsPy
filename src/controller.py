import database as db
import re
import functools
import r_type as r
import i_type as i
import j_type as j
import misc as m
import baseConverter as cv
import sim_regs
from datetime import datetime
import sim_mem

__author__ = "Elnifio"

def advance_pc(sim_regs):
    if not ("PC" in sim_regs):
        raise ValueError("Program Counter not found, please check your configuration.")
    sim_regs["PC"] = cv.dec_to_hex(cv.hex_to_dec(sim_regs["PC"]) + 4)

def control(command, sim_mems, sim_regs):
    command = command.replace(",", "")
    cmd_list = re.split(r'\s+', command)
    if len(cmd_list) == 1:
        m.syscall(sim_regs, sim_mems)
        advance_pc(sim_regs)
    else:
        inst = cmd_list[0]
        if not ((inst in db.R_TYPE) or (inst in db.I_TYPE) or (inst in db.J_TYPE)):
            raise ValueError("Unrecognizable Instruction \"" + command + "\"")
        else:
            if inst in db.R_TYPE:
                if inst == "add":
                    r.add(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "addu":
                    r.addu(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "and":
                    r.and_unambiguous(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "jr":
                    r.jr(cmd_list, sim_regs)
                elif inst == "mult":
                    r.mult(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "mfhi":
                    r.mfhi(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "mflo":
                    r.mflo(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "nor":
                    r.nor(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "or":
                    r.or_unambiguous(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "slt":
                    r.slt(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "sll":
                    r.sll(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "srl":
                    r.srl(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "sra":
                    r.sra(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                else:
                    raise ValueError("If you see this message, please report to me on Github. ")
            elif inst in db.I_TYPE:
                if inst == "addi":
                    i.addi(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "addiu":
                    i.addiu(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "andi":
                    i.andi(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "beq":
                    i.beq(cmd_list, sim_regs)
                elif inst == "bne":
                    i.bne(cmd_list, sim_regs)
                elif inst == "lui":
                    i.lui(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "lb":
                    i.lb(cmd_list, sim_regs, sim_mems)
                    advance_pc(sim_regs)
                elif inst == "sb":
                    i.sb(cmd_list, sim_regs, sim_mems)
                    advance_pc(sim_regs)
                elif inst == "lw":
                    i.lw(cmd_list, sim_regs, sim_mems)
                    advance_pc(sim_regs)
                elif inst == "sw":
                    i.sw(cmd_list, sim_regs, sim_mems)
                    advance_pc(sim_regs)
                elif inst == "ori":
                    i.ori(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                elif inst == "slti":
                    i.slti(cmd_list, sim_regs)
                    advance_pc(sim_regs)
                else:
                    raise ValueError("If you see this message, please report to me on Github. ")
            elif inst in db.J_TYPE:
                if inst == "j":
                    j.jump(cmd_list, sim_regs)
                elif inst == "jal":
                    j.jal(cmd_list, sim_regs)
                else:
                    raise ValueError("If you see this message, please report to me on Github. ")
                pass
            else:
                raise ValueError("If you see this message, please report to me on Github. ")
                    

def test():
    MAX = 10000
    regs = sim_regs.Register()
    mems = sim_mem.Memory(0x100)
    # insts = {
    #     "0x00003000": "andi $10, $10, -1",
    #     "0x00003004": "addi $10, $10, 1",
    #     "0x00003008": "beq $10, $8, 0x1",
    #     "0x0000300C": "jr $31"
    # }
    insts = {
        "0x00003000": "addi $5, $0, 3",
        "0x00003004": "addi $4, $0, 0",
        "0x00003008": "addi $2, $0, 8", 
        "0x0000300C": "syscall",
        "0x00003010": "lw $10, 0($0)",
    }
    print(regs.getRegs())
    # print(mems.getMem())
    counter = 0
    while (regs["PC"] in insts and counter < MAX):
        control(insts[regs["PC"]], mems, regs)
        counter += 1
            # raise ValueError("Unexpected Infinite Loop")
    print(regs.getRegs())
    # print(mems.get_mem_by_word(0x0))
    print(counter)

if __name__ == "__main__":
    start = datetime.now().timestamp()
    test()
    end = datetime.now().timestamp()
    print(end - start)
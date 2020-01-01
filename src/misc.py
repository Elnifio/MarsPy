import database as db
import functools
import baseConverter as cv
import Termination

__author__ = "Elnifio"

def syscall(sim_regs, sim_mems):
    v0 = "$v0"
    MAX = 100
    if not v0 in sim_regs:
        v0 = "$2"
        if not v0 in sim_regs:
            raise ValueError("No $v0 found, please check your configurations.")
    indicator = cv.hex_to_dec(sim_regs[v0])
    if indicator == 1:
        a0 = "$a0"
        if not a0 in sim_regs:
            a0 = "$4"
            if not a0 in sim_regs:
                raise ValueError("No $a0 found, please check your configurations.")
        print(cv.hex_to_dec(sim_regs[a0]), end="")
    elif indicator == 4:
        a0 = "$a0"
        if not a0 in sim_regs:
            a0 = "$4"
            if not a0 in sim_regs:
                raise ValueError("No $a0 found, please check your configurations. ")
        counter = 0
        start_address = cv.hex_to_dec(sim_regs[a0])
        val = chr(cv.hex_to_dec(sim_mems.get_mem_by_byte(start_address)))
        out = ""
        while (val != "\0" and counter < MAX):
            val = chr(cv.hex_to_dec(sim_mems.get_mem_by_byte(start_address + counter)))
            out = out + val
            counter += 1
        print(out, end="")
    elif indicator == 5:
        value = int(input())
        sim_regs[v0] = cv.dec_to_hex(value)
    elif indicator == 8:
        a0 = "$a0"
        if not a0 in sim_regs:
            a0 = "$4"
            if not a0 in sim_regs:
                raise ValueError("No $a0 found, please check your configurations. ")
        a1 = "$a1"
        if not a1 in sim_regs:
            a1 = "$5"
            if not a1 in sim_regs:
                raise ValueError("No $a1 found, please check your configurations. ")
        read_length = cv.hex_to_dec(sim_regs[a1])
        start_address = cv.hex_to_dec(sim_regs[a0])
        value = input()[:read_length]
        if len(value) < read_length:
            value = value + "\n"
        counter = 0
        for x in value:
            x_ascii = ord(x)
            sim_mems.set_mem_by_byte(start_address + counter, cv.dec_to_hex(x_ascii))
            counter += 1
    elif indicator == 10:
        raise Termination.Termination("System exited with Code 10")
    else:
        raise ValueError("Unsupported Syscall Operation. Currently support syscall 1, 4, 5, 8, and 10")
        
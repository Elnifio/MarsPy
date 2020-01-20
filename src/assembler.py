from sim_mem import Memory
from sim_mem_2 import Mem
import os, re, functools, model
import baseConverter as cv
from parser import path, registers, numeric_registers, find_register, get_decimal_value
from parse import *


"""
This serves as a substitution for parser.py
Not yet completed
"""

__author__ = "Elnifio"


def decompose(contents):
    memory_labels = {}
    instruction_labels = {}
    program_counter = "0x00003000"
    memory = Memory()
    mem_address = 0

    pass


def setupMemory(instruction, memory, mem_address, memory_labels):
    pass


def parseAsciiz(input_string):
    pass

def read_memory(instruction, memory, start_address):
    val_name = ""
    val_type = ""
    val_value = []
    comment = ""
    counter = 0
    quote_counter = 0
    value_counter = 0
    type_indicator = False
    value_indicator = False
    comment_indicator = False
    while counter < len(instruction):
        if instruction[counter] == ":":
            break
        val_name += instruction[counter]
        counter += 1
    while counter < len(instruction):
        if instruction[counter] == ".":
            type_indicator = True
        elif instruction[counter] == " " and type_indicator:
            break
        if type_indicator:
            val_type += instruction[counter]
        counter += 1
    if val_type == ".asciiz":
        value_indicator = True
        val_value = parseAsciiz(instruction[counter:])
        val_value.append("")
        while counter < len(instruction):
            if instruction[counter] != " ":
                break
            counter += 1
        while counter < len(instruction):
            char_at_position = instruction[counter]
            if char_at_position == "#" and (quote_counter & 1 == 0):
                comment_indicator = True
                break
            elif char_at_position == '"':
                if instruction[counter-1] != '\\':
                    quote_counter += 1
                    if quote_counter & 1 == 0:
                        value_indicator = False
                    elif quote_counter & 1 != 0:
                        value_indicator = True
                        value_counter += 1
                        val_value.append("")
                    counter += 1
                    continue
            elif char_at_position == "\\":
                char_at_position = instruction[counter:counter + 2]
                print("%r" % char_at_position)
                counter += 1
            if value_indicator:
                val_value[value_counter] += char_at_position
            counter += 1
        print(str(val_value))
        for value in val_value:
            if not value == "":
                print("Storing value [" + value + "] at address [" + hex(start_address) + "]")
                start_address = memory.store_string_at_address(start_address, value)
                # start_address += (get_string_len(value) + 1) 
                print("Current address is " + hex(start_address))
                

def get_string_len(in_str):
    counter = 1
    out = ""
    while counter < len(in_str) - 1:
        if in_str[counter] == "\\":
            if in_str[counter-1] != "\\":
                counter += 1
                continue
        out += in_str[counter]
        counter += 1
    return len(out)


if __name__ != "__main__":
    if not path in os.listdir("."):
        os.mkdir("mips")
    f_name = input("Please enter the file name. ")
    contents = ""
    with open(path + "/" + f_name, 'r') as f:
        contents = f.read().split("\n")
else:
    content = ""
    with open("test.asm", "r") as f:
        content = f.read().split("\n")
    mem = 0x0
    a = Mem()
    read_memory(content[0], a, mem)
    a.print_ascii_dict(0x50)
    # read_memory(content[1])



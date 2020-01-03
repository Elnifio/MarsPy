from sim_mem import Memory
import os, re, functools, model
import baseConverter as cv
from parser import path, registers, numeric_registers, find_register, get_decimal_value


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


def read_memory(instruction):
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
                if instruction[counter-1] != "\\":
                    quote_counter += 1
            val_value[0] += char_at_position
            counter += 1
    print(val_name + " --- " + val_type + " --- " + str(val_value))


if __name__ != "__main__":
    if not path in os.listdir("."):
        os.mkdir("mips")
    f_name = input("Please enter the file name. ")
    contents = ""
    with open(path + "/" + f_name, 'r') as f:
        contents = f.read().split("\n")
else:
    read_memory("asterisk: .asciiz \"*\"")
    read_memory("space: .space 84")
    read_memory("word: .ascii \"*\"")
    read_memory("word: .word 0x0000000, 0x00000000")



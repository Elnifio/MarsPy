import os
import re
import functools
import baseConverter as cv

__author__ = "Elnifio"
path = "mips"
registers = {
    "$0": "$0",
    "$at": "$1",
    "$v0": "$2",
    "$v1": "$3",
    "$a0": "$4",
    "$a1": "$5",
    "$a2": "$6",
    "$a3": "$7",
    "$t0": "$8",
    "$t1": "$9",
    "$t2": "$10",
    "$t3": "$11",
    "$t4": "$12",
    "$t5": "$13",
    "$t6": "$14",
    "$t7": "$15",
    "$s0": "$16",
    "$s1": "$17",
    "$s2": "$18",
    "$s3": "$19",
    "$s4": "$20",
    "$s5": "$21",
    "$s6": "$22",
    "$s7": "$23",
    "$t8": "$24",
    "$t9": "$25",
    "$k0": "$26",
    "$k1": "$27",
    "$gp": "$28",
    "$sp": "$29",
    "$fp": "$30",
    "$ra": "$31"
}
numeric_registers = ["$" + str(x) for x in range(32)]


def find_register(reg_name):
    if reg_name in numeric_registers:
        return reg_name
    if not reg_name in registers:
        print(reg_name)
        raise ValueError("Invalid register " + reg_name)
    return registers[reg_name]


def get_decimal_value(in_num):
    if "0x" in in_num:
        return int(in_num, 16)
    elif "0b" in in_num: 
        return int(in_num, 2)
    else:
        try:
            return int(in_num)
        except ValueError as e:
            raise ValueError(in_num + " is not a valid integer input.")


def out_to_string(out_command):
    return functools.reduce(lambda x, y: x + "\n" + y, out_command)


def append_tab(indent_num):
    return functools.reduce(lambda x, y: x + y, [" " for x in range(indent_num<<2)])


def strip_comment(in_string):
    out_string = ""
    counter = 0
    quote_counter = 0
    while counter < len(in_string):
        char_at_position = in_string[counter]
        if char_at_position == "#" and (quote_counter & 1 == 0):
            break
        elif char_at_position == '"':
            if in_string[counter-1] != "\\":
                quote_counter += 1
        out_string += char_at_position
        counter += 1
    return out_string


def parse(file_name):
    contents = ""
    with open(path + "/" + file_name, 'r') as f:
        contents = f.read().split("\n")
    contents = [x.replace("\t", " ") for x in contents]
    memory_labels = {}
    instruction_labels = {}
    program_counter = "0x00003000"
    mem_name = "memory"
    mem_address = 0
    cmd_list = []
    cmd_list.append("import sim_mem, model")
    cmd_list.append("def " + file_name[:-4] + "():")
    cmd_list.append(append_tab(1) + mem_name + " = sim_mem.Memory()")
    line_counter = 0
    # parseData(contents[8], cmd_list, memory_labels, mem_address, mem_name)
    # parseData(contents[9], cmd_list, memory_labels, mem_address, mem_name)
    # print(cmd_list)
    # return
    while line_counter < len(contents):
        cmd = contents[line_counter]
        cmd = strip_comment(cmd).strip()
        line_counter += 1
        if ".data" in cmd or cmd == "" or re.match(r'\s+', cmd):
            continue
        elif ".text" in cmd:
            break
        else:
            mem_address = parseData(cmd, cmd_list, memory_labels, mem_address, mem_name)
    cmd_list.append(append_tab(1) + "insts = {")
    line_counter_backup = line_counter
    while line_counter < len(contents):
        cmd = contents[line_counter]
        cmd = strip_comment(cmd).strip()
        line_counter += 1
        if re.match(r'\w+\:', cmd):
            instruction_labels[cmd[:-1]] = program_counter
        elif cmd == "":
            continue
        else:
            program_counter = cv.dec_to_hex(cv.hex_to_dec(program_counter) + 4)
    line_counter = line_counter_backup
    program_counter = "0x00003000"
    while line_counter < len(contents):
        cmd = contents[line_counter]
        cmd = strip_comment(cmd).strip()
        line_counter += 1
        if re.match(r'\w+\:', cmd) or cmd == "":
            continue
        else:
            out_instruction, program_counter = parseInstruction(cmd, cmd_list, memory_labels, instruction_labels, program_counter)
            cmd_list.append(append_tab(1) + out_instruction)
    cmd_list.append(append_tab(1) + "}")
    cmd_list.append(append_tab(1) + "")
    cmd_list.append(append_tab(1) + "model.run_instructions(insts, " + mem_name + ", [])")
    cmd_list.append("")
    cmd_list.append("")
    cmd_list.append("if __name__ == \"__main__\":")
    cmd_list.append(append_tab(1) + file_name[:-4] + "()")
    return out_to_string(cmd_list)

# --------
# These Functions are used to parse .data segments (storing items into memory)
def parseData(input_string, command_list, memory_labels, start_address, mem_name):
    input_list = re.split(r'\s+', input_string.replace(",", " "))
    var_name = input_list[0][:-1]
    var_type = input_list[1]
    var_value = input_list[2:]
    out_command = ""
    curr_address = start_address
    if var_type == ".asciiz":
        out_command, curr_address = parseAsciiz(var_name, var_value, memory_labels, mem_name, curr_address)
        command_list.append(append_tab(1) + out_command)
    elif var_type == ".ascii":
        out_command, curr_address = parseAscii(var_name, var_value, memory_labels, mem_name, curr_address)
        command_list.append((append_tab(1) + out_command))
    elif var_type == ".word":
        out_commands = ""
        if len(var_value) == 1:
            out_commands, curr_address = parseSingleWord(var_name, var_value, memory_labels, mem_name, curr_address)
        else: 
            out_commands, curr_address = parseWord(var_name, var_value, memory_labels, mem_name, curr_address)
        for cmd in out_commands:
            command_list.append(append_tab(1) + cmd)
    elif var_type == ".space":
        out_command, curr_address = parseSpace(var_name, var_value, memory_labels, mem_name, start_address)
        command_list.append(append_tab(1) + out_command)
    return curr_address


def parseAsciiz(var_name, var_value, memory_labels, mem_name, start_address):
    if var_value[0] == '"' and var_value[1] == '"':
        var_value[0] = '" "'
    elif len(var_value) > 1:
        var_value[0] = functools.reduce(lambda x, y: x + " " + y, var_value)
    out_command = mem_name + ".store_string_at_address(" + hex(start_address) + ", " + var_value[0] + ")"
    out_command = out_command + " # " + var_name + " " + var_value[0] + " stored at address " + hex(start_address)
    raw_string = var_value[0][1:-1]
    raw_string = raw_string.replace("\\", "")
    end_address = start_address + len(raw_string) + 1
    memory_labels[var_name] = hex(start_address)
    return out_command, end_address


def parseAscii(var_name, var_value, memory_labels, mem_name, start_address):
    if var_value[0] == '"' and var_value[1] == '"':
        var_value[0] = '" "'
    elif len(var_value) > 1:
        var_value[0] = functools.reduce(lambda x, y: x + " " + y, var_value)
    out_command = mem_name + ".store_string_at_address_without_terminator(" + hex(start_address) + ", " + var_value[0] + ")"
    out_command += (" # " + var_name + " " + var_value[0] + "stored at address " + hex(start_address) + " without terminator. ")
    raw_string = var_value[0][1:-1]
    raw_string = raw_string.replace("\\", "")
    end_address = start_address + len(raw_string)
    memory_labels[var_name] = hex(start_address)
    return out_command, end_address


def parseSingleWord(var_name, var_value, memory_labels, mem_name, start_address):
    cmd_list = []
    while start_address & 3 != 0:
        start_address += 1
    memory_labels[var_name] = hex(start_address)
    cmd_list.append(mem_name + ".store_integer_at_address(" + hex(start_address) + ", " + hex(get_decimal_value(var_value[0])) + ")")
    cmd_list[0] += (" # Allocate word for " + var_name + ", starting at address "  + hex(start_address))
    start_address += 4
    return cmd_list, start_address


def parseWord(var_name, var_value, memory_labels, mem_name, start_address):
    cmd_list = []
    list_declaration = var_name + " = ["
    for value in var_value:
        decimal_value = get_decimal_value(value)
        list_declaration += (cv.dec_to_hex(decimal_value) + ", ")
    list_declaration = list_declaration[:-2] + "]"
    while start_address & 3 != 0:
        start_address += 1
    cmd_list.append("# Allocate Words for " + var_name + ", starting at address " + hex(start_address))
    cmd_list.append(list_declaration)
    memory_labels[var_name] = hex(start_address)
    cmd_list.append("current_address = " + str(start_address))
    cmd_list.append("for x in " + var_name + ":")
    cmd_list.append(append_tab(1) + mem_name + ".store_integer_at_address(current_address, x)")
    cmd_list.append(append_tab(1) + "current_address += 4")
    start_address += 4 * len(var_value)
    return cmd_list, start_address
    

def parseSpace(var_name, var_value, memory_labels, mem_name, start_address):
    space_size = get_decimal_value(var_value[0])
    while start_address & 3 != 0:
        start_address += 1
    memory_labels[var_name] = hex(start_address)
    out_command = mem_name + ".allocate_space(" + hex(start_address) + ", " + hex(space_size) + ")"
    out_command += (" # " + str(space_size) + " space allocated for " + var_name + ", starting at " + hex(start_address))
    end_address = start_address + space_size
    return out_command, end_address
# --------

# --------
# These functions are used to parse .text segments (creating instructions)
def parseInstruction(input_string, command_list, memory_labels, instruction_labels, program_counter):
    cmd_list = re.split(r'\s+', input_string.replace(",", " "))
    instruction = cmd_list[0]
    out_instruction = ""
    if (instruction == "lw" or instruction == "sw" or instruction == "lb" or instruction == "sb"):
        out_instruction = parseLoadStore(cmd_list, memory_labels)    
    elif (instruction == "bne" or instruction == "beq"): 
        out_instruction = parseBranch(cmd_list, instruction_labels, program_counter)
    elif (instruction == "j" or instruction == "jal"):
        out_instruction = parseJump(cmd_list, instruction_labels)
    # elif (instruction == "li"):
    #     out_instruction, program_counter = parseLoadImmediate(cmd_list, program_counter)
    # elif (instruction == "la"):
    #     out_instruction, program_counter = parseLoadAddress(cmd_list, program_counter, memory_labels)
    else:
        out_instruction = parseOther(cmd_list)
    out_instruction = (append_tab(1) + "\"" + program_counter + "\": \"") + out_instruction + "\","
    new_program_counter = cv.dec_to_hex(cv.hex_to_dec(program_counter) + 4) # TODO return the new program counter
    return out_instruction, new_program_counter


def parseLoadStore(input_list, memory_labels):
    out_instruction = input_list[0] + " "
    out_instruction += (find_register(input_list[1]) + ", ")
    # Addresses situations for "lw $t0, 120"
    if re.match(r'^[0-9\-][0-9\-xabcdefABCDEF]+$', input_list[2]): 
        out_instruction += (input_list[2] + "($0)")
    # Addresses situations for "lw $t0, width"
    elif re.match(r'^[0-9A-Za-z\_\$]+$', input_list[2]): 
        if not input_list[2] in memory_labels:
            raise ValueError("Address label " + input_list[2] + " not found. ")
        else:
            out_instruction += (memory_labels[input_list[2]] + "($0)")
    # Addresses situations for "lw $t0, width($t1)"
    else:
        address_list = re.split(r'[\(\)]', input_list[2])
        numeric_address = ""
        if address_list[0] in memory_labels:
            # Numeric lables should not be allowed since it would cause confusion
            numeric_address = memory_labels[address_list[0]] 
        else:
            # Addresses situations for "lw $t0, 0x02($0)"
            # Cannot Recognizes if the label is not in memory_labels, 
            # Cannot Recognizes 2's Complement hex addresses
            numeric_address = address_list[0] 
        out_instruction += (numeric_address + "(" + find_register(address_list[1]) + ")")
    return out_instruction


def parseBranch(input_list, instruction_labels, program_counter):
    out_instruction = input_list[0] + " " + find_register(input_list[1]) + ", " + find_register(input_list[2]) + ", "
    branch_label = input_list[3]
    if not branch_label in instruction_labels:
        raise ValueError("The offset label " + branch_label + " is not valid")
    else:
        branch_address = cv.hex_to_dec(instruction_labels[branch_label])
        curr_address = cv.hex_to_dec(program_counter)
        offset = (branch_address - curr_address - 4)>>2
        out_instruction += (str(offset))
    return out_instruction
    

def parseJump(input_list, instruction_labels): 
    out_instruction = input_list[0] + " "
    jump_target = input_list[1]
    if not jump_target in instruction_labels:
        raise ValueError("Invalid Jump Target " + jump_target)
    else:
        out_instruction += cv.dec_to_hex(cv.hex_to_dec(instruction_labels[jump_target]) >> 2)
    return out_instruction


def parseLoadImmediate(input_list, program_counter):
    immediate_literal = input_list[2]
    immediate_value = 0
    if immediate_literal.startswith("0x") and len(immediate_literal) == 10:
        immediate_value = cv.hex_to_dec(immediate_literal)
    else:
        immediate_value = get_decimal_value(immediate_literal)
    print(input_list)
    print(immediate_value)
    return "", program_counter
    pass


def parseLoadAddress(input_list, program_counter, memory_labels):
    pass


def parseOther(input_list):
    out_instruction = input_list[0] + " "
    if input_list[0] == "syscall":
        return out_instruction.strip()
    else:
        if input_list[0] == "li" or input_list[0] == "la":
            print("You are using Pseudo Instructions for " + str(input_list) + ", but this parser cannot recognize these. We recommend you to replace them with addi.")
        counter = 1
        while counter < len(input_list):
            argument = input_list[counter]
            if argument[0] == "$":
                out_instruction += find_register(argument)
            else:
                out_instruction += argument
            if counter != len(input_list) - 1:
                out_instruction += ", "
            counter += 1
    return out_instruction.strip()


if __name__ == "__main__":
    if not path in os.listdir("."):
        os.mkdir("mips")
    f_name = input("Please enter the file name:")
    f_py = parse(f_name)
    if f_py != None: 
        with open(path + "/" + f_name[:-4] + ".py", "w") as f:
            f.write(f_py)

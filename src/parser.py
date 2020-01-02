import os
import re
import functools
import baseConverter as cv


"""
This module parses the .asm file to .py file. 
If you wish to parse, please first move the file you need to parse to `./mips` folder, and enter `python3 parser.py` and then enter the full name of the file you wish to parse.
You should then move the generated .py file to the same folder with sim_mem.py and run it using `python3 $FILE_NAME.py`

For instance, if you wish to parse and run "./mips/sum.asm", you should first enter `python3 parser.py`, and enter `sum.asm`. 
After the .py file has generated, move it to `.` folder, and then type `python3 sum.py` to run. 
"""


__author__ = "Elnifio"
# This defines the folder that contains the source .asm file
path = "mips"
# This defines all register alias. Each element is a key-value set of Alias - Original Names
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
# This defines the list of registers' original names (such as "$31")
numeric_registers = ["$" + str(x) for x in range(32)]


# This method is used to find registers' original name given the register's alias
# @Param: reg_name: a string representing the register's name.
# Returns: the register's original name
# Raises: ValueError if this is not a valid register's original name or alias
def find_register(reg_name):
    if reg_name in numeric_registers:
        return reg_name
    if not reg_name in registers:
        raise ValueError("Invalid register " + reg_name)
    return registers[reg_name]


# This method is used to convert string to number. 
# @Param: in_num: string as a hex/decimal/binary representation of an integer
# Return: integer
# Raises: ValueError if the in_num cannot be converted to integer. 
# Notice that this method cannot convert 2's Complement representation. 
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


# This method is used to concatenate all strings in out_command with "\n"
# @Param: out_command: a list of strings that contains strings that needs to be concatenated
# Return: a string
def out_to_string(out_command):
    return functools.reduce(lambda x, y: x + "\n" + y, out_command)


# This method is used to append tabs to a string. 
# @Param: indent_num representing the number of tabs that needs to be appended
# Return: a string
def append_tab(indent_num):
    return functools.reduce(lambda x, y: x + y, [" " for x in range(indent_num<<2)])


# Strips the comment in a string. All contents after "#" pound character are considered comments.
# @Param: The input string that needs to be stripped.
# Return: string with comments stripped.
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


# Parses the file `./mips/$FILE_NAME`
# @Param: the file name, including .asm
# Return: a string which should be then written to a .py file.
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

# Parses .data segments
# @Params: 
#                   input_string: the string that needs to be parsed
#                   command_list: list, output commands will be appended to this list. 
#                   memory_labels: dictionary, containing all memory labels defined in the .asm file. 
#                                               Every element of memory_labels should be a Label-Address (hexadecimal) set
#                   start_address: integer, the current start address of the memory. Each time a value is stored, the start_address should be updated. 
#                                               For instance, if the start_address is "0x00", and a .asciiz is stored, then the current address should be "0x02", which is the new start_address
#                   mem_name: the name of the memory
# Return: new_address which is the new address after storing particular contents. 
# Could only recognize .ascii, .asciiz, .word, and .space
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


# Parses .asciiz values. 
# @Params: 
#                   var_name: the variable label
#                   var_value: the variable value
#                   memory_labels: a dictionary. The key set <var_name: start_address> will be put into it
#                   mem_name: name of the memory
#                   start_address: integer, the current start address of the memory. 
# Returns: 
#                   out_command: string, the command generated based on MIPS instruction.
#                   end_address: integer, the new address after storing the string
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


# Parses .ascii values
# Same as above. 
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


# Parses .word values for storing a single word.
# @Params same as above
# Returns:
#                   cmd_list: a list containing parsed instructions. Each element is a string
#                   start_address: same as above.
def parseSingleWord(var_name, var_value, memory_labels, mem_name, start_address):
    cmd_list = []
    while start_address & 3 != 0:
        start_address += 1
    memory_labels[var_name] = hex(start_address)
    cmd_list.append(mem_name + ".store_integer_at_address(" + hex(start_address) + ", " + hex(get_decimal_value(var_value[0])) + ")")
    cmd_list[0] += (" # Allocate word for " + var_name + ", starting at address "  + hex(start_address))
    start_address += 4
    return cmd_list, start_address


# Parses .word values for storing multiple words
# @Params same as above
# Returns same as above
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
    

# Parses .space
# @Params same as above
# Return values same as parseAscii & parseAsciiz
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

# parse .text segments
# @Params: 
#                   input_string: the instruction 
#                   command_list: list, output commands will be appended to this list. 
#                   memory_labels: dictionary, containing all memory labels defined in the .asm file. 
#                                               Every element of memory_labels should be a Label-Address (hexadecimal) set
#                   instruction_labels: dictionary, containing all instruction labels defined in the .asm file. 
#                                               Every element of instruction_labels should be a Label-Address (hexadecimal) set
#                   program_counter: the program counter (essentially the "instruction memory counter") which counts the address of the instruction. 
# Returns: 
#                   out_instruction: string, the command generated from MIPS instruction
#                   new_program_counter: the updated program_counter ("instruction memory counter")
# Notice that the Load Immediate and Load Address instruction not implemented yet. 
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
    new_program_counter = cv.dec_to_hex(cv.hex_to_dec(program_counter) + 4)
    return out_instruction, new_program_counter


# Parses lw, lb, sw, sb instructions
# @Params: 
#                   input_list: represents an array containing separated parts of the instruction. For instance, 
#                                       "addi $8, $9, 12" -> ["addi", "$8", "$9", "12"]
#                                       "lw $8, 0x04($12)" -> ["lw", "$8", "0x04($12)"]
#                                       "mult $8, $9" -> ["mult", "$8", "$9"]
#                   memory_labels: dictionary, containing all memory labels defined in the .asm file. 
#                                               Every element of memory_labels should be a Label-Address (hexadecimal) set
# Return: out_command: string, the command generated based on MIPS instruction.
# Raises: ValueError if cannot find address labels
# Cannot Recognizes if the label is not in memory_labels
# Cannot Recognizes 2's Complement hex addresses
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
            numeric_address = address_list[0] 
        out_instruction += (numeric_address + "(" + find_register(address_list[1]) + ")")
    return out_instruction


# Parses bne & beq instructions
# @Params: 
#                   input_list: represents an array containing separated parts of the instruction. For instance, 
#                                       "addi $8, $9, 12" -> ["addi", "$8", "$9", "12"]
#                                       "lw $8, 0x04($12)" -> ["lw", "$8", "0x04($12)"]
#                                       "mult $8, $9" -> ["mult", "$8", "$9"]
#                   memory_labels: dictionary, containing all memory labels defined in the .asm file. 
#                                               Every element of memory_labels should be a Label-Address (hexadecimal) set
#                   instruction_labels: dictionary, containing all instruction labels defined in the .asm file. 
#                                               Every element of instruction_labels should be a Label-Address (hexadecimal) set
# Return: same as above
# Raises: ValueError if the label does not exist in instruction_labels
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
    

# Parses j & jal instructions
# @Params: 
#                   input_list: represents an array containing separated parts of the instruction. For instance, 
#                                       "addi $8, $9, 12" -> ["addi", "$8", "$9", "12"]
#                                       "lw $8, 0x04($12)" -> ["lw", "$8", "0x04($12)"]
#                                       "mult $8, $9" -> ["mult", "$8", "$9"]
#                   instruction_labels: dictionary, containing all instruction labels defined in the .asm file. 
#                                               Every element of instruction_labels should be a Label-Address (hexadecimal) set
# Return: same as above
# Raises: ValueError if the label does not exist in instruction_labels
def parseJump(input_list, instruction_labels): 
    out_instruction = input_list[0] + " "
    jump_target = input_list[1]
    if not jump_target in instruction_labels:
        raise ValueError("Invalid Jump Target " + jump_target)
    else:
        out_instruction += cv.dec_to_hex(cv.hex_to_dec(instruction_labels[jump_target]) >> 2)
    return out_instruction


# Parses Load Immediate Pseudo-code
# Did not implement yet
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


# Parses the Load Address Pseudo-code
# Did not implement yet
def parseLoadAddress(input_list, program_counter, memory_labels):
    pass


# Parses all other instructions.
# @Params:
#                   input_list: represents an array containing separated parts of the instruction. For instance, 
#                                       "addi $8, $9, 12" -> ["addi", "$8", "$9", "12"]
#                                       "lw $8, 0x04($12)" -> ["lw", "$8", "0x04($12)"]
#                                       "mult $8, $9" -> ["mult", "$8", "$9"]
# Return: same as above
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

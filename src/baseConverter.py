import functools

"""
This module is used to calculate and convert numbers in different bases. 
"""

__author__ = "Elnifio"

# Converts a binary number ("0b" stripped) to decimal, using 2's Complement
# @Params: in_num: a string containing only 0 and 1 ("0b" stripped)
# Return: a integer which is calculated from in_num using 2's Complement calculation
def bin_to_dec(in_num):
    out = -(2**(len(in_num) - 1)) * int(in_num[0])
    out += bin_to_dec_unsigned(in_num[1:])
    return out

# Converts (groups) a binary number ("0b" stripped) to hexadecimal (including "0x")
# @Params: in_num: a string containing only 0 and 1 ("0b" stripped)
# Return: a hexadecimal value (including "0x")
def bin_to_hex(in_num):
    out = ""
    for n in [in_num[x:x+4] for x in range(len(in_num)) if x&3 == 0]:
        n = "0b" + n
        out = out + hex(int(n, 2))[-1]
    return "0x" + out.upper()

# Converts hexadecimal (starts with "0x") to a binary number ("0b" stripped)
# @Params: in_num: a string representing a 32-bit hexadecimal number (including "0x")
# Return: a binary series not including "0b"
def hex_to_bin(in_num):
    out = ""
    in_num = in_num[2:]
    for n in in_num:
        x = "0x" + n
        out = out + dec_to_bin(int(n, 16))[-4:]
    return out

# Converts a binary series to a unsigned decimal number
# @Params: in_num:  a binary series not including "0b"
# Return: A non-negative decimal integer
def bin_to_dec_unsigned(in_num):
    out = int("0b" + in_num, 2)
    return out
    
# Converts a decimal number to its binary value, in 2's Complement representation.
# @Params: in_num: a decimal integer; base: length of the output series, default set to 32. 
# Return: A binary series not including "0b"
# For instance, dec_to_bin(-1, 4) = "1111"; dec_to_bin(32, 4) = "0000" 
def dec_to_bin(in_num, base=32):
    out_arr = bin(in_num & int(bin(2**base - 1), 2))[2:]
    return out_arr.zfill(base)

# Converts an integer directly to its hexadecimal representation
# @ Params: in_num: an integer
# Return: A hex string including "0x"
def dec_to_hex(in_num):
    return bin_to_hex(dec_to_bin(in_num))

# Converts a hexadecimal string directly to an integer, using 2's Complement
# @Params: in_num: A hexadecimal string in 2's Complement
# Return: an integer
def hex_to_dec(in_num):
    return bin_to_dec(hex_to_bin(in_num))
    
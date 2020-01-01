import functools

__author__ = "Elnifio"

def bin_to_dec(in_num):
    out = -(2**(len(in_num) - 1)) * int(in_num[0])
    out += bin_to_dec_unsigned(in_num[1:])
    return out

def bin_to_hex(in_num):
    out = ""
    for n in [in_num[x:x+4] for x in range(len(in_num)) if x&3 == 0]:
        n = "0b" + n
        out = out + hex(int(n, 2))[-1]
    return "0x" + out.upper()

def hex_to_bin(in_num):
    out = ""
    in_num = in_num[2:]
    for n in in_num:
        x = "0x" + n
        out = out + dec_to_bin(int(n, 16))[-4:]
    return out


def bin_to_dec_unsigned(in_num):
    out = int("0b" + in_num, 2)
    return out
    

def dec_to_bin(in_num, base=32):
    out_arr = bin(in_num & int(bin(2**base - 1), 2))[2:]
    return out_arr.zfill(base)

def dec_to_hex(in_num):
    return bin_to_hex(dec_to_bin(in_num))

def hex_to_dec(in_num):
    return bin_to_dec(hex_to_bin(in_num))

def testBTD():
    a = -31225
    a = dec_to_bin(a, 64)
    print(a)
    print(bin_to_hex(a))
    print(bin_to_dec(a))
    print(bin_to_dec_unsigned(a))

def testDTB():
    a = -15
    print(dec_to_bin(a))
    a = 15
    print(dec_to_bin(a))
    a = 0x5678ABCD
    print(a)
    print(len(dec_to_bin(a)))
    print(dec_to_bin(a))
    print(bin_to_hex(dec_to_bin(a)))
    print(dec_to_hex(a))

if __name__ == "__main__":
    testBTD()

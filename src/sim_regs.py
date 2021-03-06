"""
A Simulated Register. Notice that it essentially is a dictionary. 
"""


__author__ = "Elnifio"


class Register(object):
    # Constructor. No parameter is required. 
    # Notice that the value of Program Counter is set to "0x00003000" by default. Other registers are set to 0
    def __init__(self):
        self.__regs = {
            "$0": "0x00000000", # $0
            "$1": "0x00000000", # $at
            "$2": "0x00000000", # $v0
            "$3": "0x00000000", # $v1
            "$4": "0x00000000", # $a0
            "$5": "0x00000000", # $a1
            "$6": "0x00000000", # $a2
            "$7": "0x00000000", # $a3
            "$8": "0x00000000", # $t0
            "$9": "0x00000000", # $t1
            "$10": "0x00000000", # $t2
            "$11": "0x00000000", # $t3
            "$12": "0x00000000", # $t4
            "$13": "0x00000000", # $t5
            "$14": "0x00000000", # $t6
            "$15": "0x00000000", # $t7
            "$16": "0x00000000", # $s0
            "$17": "0x00000000", # $s1
            "$18": "0x00000000", # $s2
            "$19": "0x00000000", # $s3
            "$20": "0x00000000", # $s4
            "$21": "0x00000000", # $s5
            "$22": "0x00000000", # $s6
            "$23": "0x00000000", # $s7
            "$24": "0x00000000", # $t8
            "$25": "0x00000000", # $t9
            "$26": "0x00000000", # $k0
            "$27": "0x00000000", # $k1
            "$28": "0x00000000", # $gp
            "$29": "0x00000000", # $sp
            "$30": "0x00000000", # $fp
            "$31": "0x00000000", # $ra
            "PC": "0x00003000", # Program Counter
            "hi" : "0x00000000", # High
            "lo": "0x00000000" # Low
        }

    # Metamethod for supporting operations such as Register()["$31"]
    def __getitem__(self, name):
        return self.__regs[name]
    
    # Metamethod for supporting operations such as Register()["$31"] = "0x00003000"
    def __setitem__(self, name, value):
        self.__regs[name] = value

    # Metamethod for supporting operations such as "$31" in Register()
    def __contains__(self, item):
        return item in self.__regs

    # Returns the dictionary itself. 
    def getRegs(self):
        return self.__regs
        
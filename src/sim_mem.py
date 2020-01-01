import baseConverter as cv
import functools

__author__ = "Elnifio"

class Memory(object):
    def __init__(self, max_val=0x3000):
        self.__mems = ["00" for x in range(max_val)]
        self.__max = max_val
    
    def __str__(self):
        return ""

    def check_validity(self, address, align=False):
        if address >= self.__max or address < 0:
            raise ValueError("Memory Address out of bound at " + hex(address))
        if align:
            if not address & 3 == 0:
                raise ValueError("Memory Address not Aligned at " + hex(address))

    def getMem(self):
        return self.__mems

    def get_mem_by_word(self, address):
        self.check_validity(address, True)
        return "0x" + functools.reduce(lambda x, y: y + x, self.__mems[address:address + 4])
    
    def set_mem_by_word(self, address, value):
        self.check_validity(address, True)
        value = value[2:].upper()
        counter = 3
        for x in [value[y:y+2] for y in range(8) if y & 1 == 0]:
            self.__mems[address + counter] = x
            counter -= 1

    def get_mem_by_byte(self, address):
        self.check_validity(address)
        return "0x000000" + self.__mems[address]
    
    def set_mem_by_byte(self, address, value):
        self.check_validity(address)
        value = value[-2:].upper()
        self.__mems[address] = value
    
    def store_string_at_address(self, address, value):
        self.check_validity(address)
        counter = 0
        for x in value:
            x_ascii = ord(x)
            self.set_mem_by_byte(address + counter, cv.dec_to_hex(x_ascii))
            counter += 1
        counter += 1
        self.set_mem_by_byte(address + counter, "0x00")

    def store_string_at_address_without_terminator(self, address, value):
        self.check_validity(address)
        counter = 0
        for x in value:
            x_ascii = ord(x)
            self.set_mem_by_byte(address + counter, cv.dec_to_hex(x_ascii))
            counter += 1

    def store_integer_at_address(self, address, value):
        self.check_validity(address)
        self.set_mem_by_word(address, cv.dec_to_hex(value))

    def allocate_space(self, start_address, length):
        self.check_validity(start_address)
        self.check_validity(start_address + length)
    
    def store_char_at_address(self, address, value):
        self.check_validity(address)
        val_ascii = ord(value)
        self.set_mem_by_byte(address, cv.dec_to_hex(val_ascii))
        self.set_mem_by_byte(address + 1, "0x00")
    
    def store_char_without_terminator_at_address(self, address, value):
        self.check_validity(address)
        val_ascii = ord(value)
        self.set_mem_by_byte(address, cv.dec_to_hex(val_ascii))

def test():
    m = Memory(0x100)
    print(len(m.getMem()))
    m.set_mem_by_word(0x4, "0x6C6C6068")
    print(m.getMem())
    print(m.get_mem_by_word(0x4))
    m.set_mem_by_byte(0x3, "0x000000FC")
    print(m.getMem())
    print(m.get_mem_by_word(0x0))
    print(m.get_mem_by_word(0x1))



if __name__ == "__main__":
    test()

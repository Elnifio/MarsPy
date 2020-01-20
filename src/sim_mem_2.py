import baseConverter as cv
import functools

"""
Another Simulated Memory.
"""

__author__ = "Elnifio"

class Mem(object):
    # Constructor for memory.
    # @Param: max_val: optional integer, defines the maximum value of memory.
    def __init__(self, max_val=0x3000):
        self.__mems = [0x00000000 for x in range(max_val>>2)]
        self.__max = max_val
        pass

    def getMem(self):
        return [cv.dec_to_hex(x) for x in self.__mems]
    
    def check_validity(self, address, align=False):
        if address >= self.__max or address < 0:
            raise ValueError("Memory Address out of bound at " + hex(address))
        if align:
            if not address & 3 == 0:
                raise ValueError("Memory Address not Aligned at " + hex(address))

    def get_mem_by_word(self, address):
        self.check_validity(address, True)
        return cv.dec_to_hex(self.__mems[address>>2])
    
    def set_mem_by_word(self, address, value):
        self.check_validity(address, True)
        if isinstance(value, int):
            self.__mems[address>>2] = value & 0xFFFFFFFF
        elif isinstance(value, str):
            self.__mems[address>>2] = cv.hex_to_dec(value)
        else:
            raise ValueError("Unsupported Type. ")

    def get_mem_by_byte(self, address):
        self.check_validity(address)
        remainder = address & 3
        mask = 0x000000FF << (remainder<<3)
        return cv.dec_to_hex((self.__mems[address>>2] & mask)>>(remainder << 3))
    
    def set_mem_by_byte(self, address, value):
        self.check_validity(address)
        remainder = address & 3
        if isinstance(value, str):
            value = (cv.hex_to_dec(value) & 0x000000FF) << (remainder << 3)
        elif isinstance(value, int):
            value = (value & 0x000000FF) << (remainder << 3)
        else: 
            raise ValueError("Unsupported Type. ")
        original_value = self.__mems[address >> 2]
        high_bytes = original_value >> ((remainder + 1) << 3)
        new_value = (high_bytes << ((remainder + 1) << 3)) | value
        mask = 0xFFFFFFFF >> ((4 - remainder) << 3)
        low_bytes = original_value & mask
        new_value = new_value | low_bytes
        self.__mems[address >> 2] = new_value
        
    def store_string_at_address(self, address, value):
        new_address = self.store_string_at_address_without_terminator(address, value)
        self.set_mem_by_byte(address + len(value), 0)
        return new_address + 1
        
    
    def store_integer_at_address(self, address, value):
        self.check_validity(address, True)
        self.set_mem_by_word(address, value)
        return address + 4

    def store_string_at_address_without_terminator(self, address, value):
        self.check_validity(address)
        counter = 0
        for x in value:
            x_ascii = ord(x)
            self.set_mem_by_byte(address + counter, x_ascii)
            counter += 1
        return address + counter
        
    def allocate_space(self, start_address, length):
        self.check_validity(start_address)
        self.check_validity(start_address + length)
        return start_address + length
    
    def store_char_at_address(self, address, value):
        self.check_validity(address)
        val_ascii = ord(value)
        self.set_mem_by_byte(address, val_ascii)
        self.set_mem_by_byte(address + 1, 0)
        return address + 2

    def get_mem_dict(self, end_address):
        if isinstance(end_address, str):
            end_address = cv.hex_to_dec(end_address)
        self.check_validity(end_address, True)
        return {cv.dec_to_hex(x):self.get_mem_by_word(x) for x in range(end_address) if x & 3 == 0}

    def get_ascii_dict(self, end_address):
        if isinstance(end_address, str):
            end_address = cv.hex_to_dec(end_address)
        self.check_validity(end_address, True)
        return {cv.dec_to_hex(x):functools.reduce(lambda a, b: b + " " + a, [chr(cv.hex_to_dec(self.get_mem_by_byte(y))) for y in range(x, x+4)]) for x in range(end_address) if x & 3 == 0}
    
    def print_mem_dict(self, end_address):
        mem_dict = self.get_mem_dict(end_address)
        for key, value in mem_dict.items():
            print(key + ": " + value)

    def print_ascii_dict(self, end_address):
        mem_dict = self.get_ascii_dict(end_address)
        for key, value in mem_dict.items():
            print("%s: %r" % (key, value))
    pass


if __name__ == "__main__":
    m = Mem()
    m.set_mem_by_word(0x4, 0x1234ABCD)
    m.set_mem_by_byte(0x5, 0x1234ABCD)
    m.set_mem_by_byte(0x6, 0x00000006)
    m.set_mem_by_byte(0x7, 0x00000007)
    m.store_string_at_address(0x0, "hello\n")
    m.store_integer_at_address(0x8, 0x00001234)
    print(m.getMem()[:10])
    print(m.get_ascii_dict(0x0C))
    m.print_ascii_dict(0x0C)
    
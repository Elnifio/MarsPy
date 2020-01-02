import baseConverter as cv
import functools


"""
A Simulated Memory. 
"""


__author__ = "Elnifio"


class Memory(object):
    # Constructor for memory. 
    # @Param: mas_val: optional integer, defines the maximum value of memory. 
    def __init__(self, max_val=0x3000):
        self.__mems = ["00" for x in range(max_val)]
        self.__max = max_val
    
    # Unused feature.
    def __str__(self):
        return ""

    # Checks the validity of address. 
    # @Params:
    #               address: the address that needs to be checked
    #               align: Optional, indicating if align should be checked
    # Returns None
    # Raises:
    #               ValueError if memory address out of bound, such as accessing 0x4003 for Memory()
    #               ValueError if memory address not aligned. This will only be checked if align is true. 
    def check_validity(self, address, align=False):
        if address >= self.__max or address < 0:
            raise ValueError("Memory Address out of bound at " + hex(address))
        if align:
            if not address & 3 == 0:
                raise ValueError("Memory Address not Aligned at " + hex(address))

    # Returns the __mems property which is a list containing all memory values. 
    # No parameters needed.
    # Return: list containing all values stored in memory. each element represents a byte.
    def getMem(self):
        return self.__mems

    # Returns the memory content at particular address by word, checks align and bound. 
    # @Param: address: integer
    # Return: a hexadecimal string containing the word stored at address
    # Raises: Refer to check_validity method
    def get_mem_by_word(self, address):
        self.check_validity(address, True)
        return "0x" + functools.reduce(lambda x, y: y + x, self.__mems[address:address + 4])
    
    # Sets memory content at particular address by word, checks align and bound. 
    # @Params:
    #               address: integer
    #               value: a hexadecimal string containing the value that needs to be stored into memory, including "0x"
    # Return: None
    # Raises: Refer to check_validity method
    def set_mem_by_word(self, address, value):
        self.check_validity(address, True)
        value = value[2:].upper()
        counter = 3
        for x in [value[y:y+2] for y in range(8) if y & 1 == 0]:
            self.__mems[address + counter] = x
            counter -= 1

    # Returns the memory content at particular address by byte, checks bound.
    # @Param: address; integer
    # Return: a hexadecimal string, containing "0x000000" + particular byte at address in hexadecimal
    # Raises: Refer to check_validity method
    def get_mem_by_byte(self, address):
        self.check_validity(address)
        return "0x000000" + self.__mems[address]
    
    # Sets the memory content at particular address by byte, checks bound. 
    # @Params:
    #               address: integer
    #               value: a hexadecimal string containing the value that needs to be stored into memory, including "0x"
    # Return: None
    # Raises: Refer to check_validity method
    # Notice that only the last byte in input value will be stored. 
    def set_mem_by_byte(self, address, value):
        self.check_validity(address)
        value = value[-2:].upper()
        self.__mems[address] = value
    
    # Stores strings into memory, adding "\0" after it.
    # @Params: 
    #               address: integer
    #               value: the string that needs to be stored into memory
    # Return: None
    # Raises: Refer to check_validity method
    def store_string_at_address(self, address, value):
        self.check_validity(address)
        counter = 0
        for x in value:
            x_ascii = ord(x)
            self.set_mem_by_byte(address + counter, cv.dec_to_hex(x_ascii))
            counter += 1
        counter += 1
        self.set_mem_by_byte(address + counter, "0x00")

    # Stores strings into memory, not adding "\0" after it.
    # Same as store_string_at_address
    def store_string_at_address_without_terminator(self, address, value):
        self.check_validity(address)
        counter = 0
        for x in value:
            x_ascii = ord(x)
            self.set_mem_by_byte(address + counter, cv.dec_to_hex(x_ascii))
            counter += 1

    # Store integers into memory. One integer occupies one word
    # @Params:
    #               address: integer
    #               Value: integer that needs to be stored into memory
    # Return: None
    # Raises: Refer to check_validity method
    def store_integer_at_address(self, address, value):
        self.check_validity(address)
        self.set_mem_by_word(address, cv.dec_to_hex(value))

    # Allocates space to memory. Notice that it actually does nothing except validating the start and end address
    # @Params: 
    #               start_address: integer
    #               length: integer, indicating the length of reserved space
    # Return: None
    # Raises: Refer to check_validity method
    def allocate_space(self, start_address, length):
        self.check_validity(start_address)
        self.check_validity(start_address + length)
    
    # Stores char to memory, adding "\0" to it.
    # @Params:
    #               address: integer
    #               value: the char that needs to be stored. 
    # Return: None
    # Raises: Refer to check_validity method and ord method
    # Notice that errors will be raised by ord() if value contains multiple characters
    def store_char_at_address(self, address, value):
        self.check_validity(address)
        val_ascii = ord(value)
        self.set_mem_by_byte(address, cv.dec_to_hex(val_ascii))
        self.set_mem_by_byte(address + 1, "0x00")
    
    # Stores char to memory, not adding "\0"
    # Same as store_char_at_address
    def store_char_without_terminator_at_address(self, address, value):
        self.check_validity(address)
        val_ascii = ord(value)
        self.set_mem_by_byte(address, cv.dec_to_hex(val_ascii))

import chip8_util as c8u
import numpy as np
import itertools as itt
import warnings

# Writing code to emulate low level hardware often requires using things like
# well modelled integer overflow. Numpy warns when this happens and thereby
# clogs the console with warnings about expected behaviour. This imperative
# prevents this.
warnings.filterwarnings('ignore')

class Chip8:
    """
    The main class for the chip 8 emulator.
    Sound, delay and graphics are omitted for ease of implementation as I'm not
    writing games but just doing computation. I've replaced them with a few
    instructions that do numerical i/o in various formats.
    """
    
    def __init__(self, code):
        """
        The default constructor for the class.
        """
        self.memory = [np.uint8(0) for _ in range(4096)]
        self.registers = [np.uint64(0) for _ in range(16)]
        self.stack = []
        self.stack_ptr = 0
        self.code_ptr = 0
        self.memory_ptr = 0

        for i, byte in enumerate(code):
            self.memory[i] = byte
        
        for i in self.memory:
            print(hex(i), end=' ')

    
    def subroutine_return(self) -> None:
        """
        Implements the 01EE opcode.
        Returns from the current subroutine, sets the instruction pointer to the
        address at the top of the call stack then pops the stack.
        """
        self.code_ptr = self.stack.pop() - 2
    
    def goto(self, address : int) -> None:
        """
        Implements the 1NNN opcode.
        Sets the instruction pointer to address and then resumes execution.
        """
        self.code_ptr = address - 2
    
    def subroutine_call(self, address : int) -> None:
        """
        Implements the 2NNN opcode.
        Calls the subroutine at address NNN.
        Pushes the code_ptr onto the call stack, then sets the code_ptr to NNN.
        """
        self.stack.append(self.code_ptr-2)
        self.code_ptr = address - 2
    
    def skip_next_if_equal_const(self,
                                 register_index : int,
                                 constant : int) -> None:
        """
        Implements the 3XNN opcode.
        Skips the next instruction if register[register_index] is equal to
        constant
        """
        if self.registers[register_index] == constant:
            self.code_ptr += 2
    
    def skip_next_if_unequal_const(self,
                                   register_index : int,
                                   constant : int) -> None:
        """
        Implements the 4XNN opcode.
        Skips the next instruction if register[register_index] is not equal to
        constant
        """
        if self.registers[register_index] != constant:
            self.code_ptr += 2

    def skip_next_if_equal(self, dest_index : int, src_index : int) -> None:
        """
        Implements the 5XY0 opcode.
        Skips the next instruction if register[dest_index] is equal to
        register[src_index]
        """
        if self.registers[dest_index] == self.registers[src_index]:
            self.code_ptr += 2
    
    def assign_const_to_register(self,
                                 dest_index : int,
                                 constant : int) -> None:
        """
        Implements the 6XNN opcode.
        Writes constant to registers[dest_index]
        """
        self.registers[dest_index] = np.uint64(constant)
    
    def add_const_to_register(self, dest_index : int, constant : int) -> None:
        """
        Implements the 7XNN opcode.
        Adds byte constant to registers[dest_index] without setting the
        carry flag.
        """
        self.registers[dest_index] += np.uint64(constant)

    def assign_register(self, dest_index : int, src_index : int) -> None:
        """
        Implements the 8XY0 opcode:
            Pseudocode: register[dest_index] = register[src_index]
        """
        self.registers[dest_index] = self.registers[src_index]
    
    def bitwise_or(self, dest_index : int, src_index : int) -> None:
        """
        Implemements the 8XY1 opcode:
            Pseudocode: register[dest_index] |= register[src_index]
        """
        self.registers[dest_index] |= self.registers[src_index]
    
    def bitwise_and(self, dest_index : int, src_index : int) -> None:
        """
        Implemements the 8XY2 opcode:
            Pseudocode: register[dest_index] &= register[src_index]
        """
        self.registers[dest_index] &= self.registers[src_index]
    
    def bitwise_xor(self, dest_index : int, src_index : int) -> None:
        """
        Implemements the 8XY3 opcode:
            Pseudocode: register[dest_index] ^= register[src_index]
        """
        self.registers[dest_index] ^= self.registers[src_index]

    def add_registers(self, dest_index : int, src_index : int) -> None:
        """
        Implements the 8XY4 opcode.
        Adds registers X and Y together and sets carry flag if needed.
            Pseudocode:
                tmp = register[dest_index] + register[src_index]
                if tmp > UINT64_MAX then
                    register[0xF] = 1
                else
                    register[0xF] = 0
                end
                register[dest_index] = tmp
        """
        tmp = self.registers[dest_index] + self.registers[src_index]
        if tmp < self.registers[dest_index]:

            self.registers[0xF] = np.uint64(1)
        else:
            self.registers[0xF] = np.uint64(0)
        self.registers[dest_index] = np.uint64(tmp)
    
    def subtract_registers(self, dest_index : int, src_index : int) -> None:
        """
        Implements the 8XY5 opcode.
        Subtracts registers X and Y together and sets the flag register if 
        there was no borrow.
            Psuedocode:
                if register[dest_index] >= register[src_index] then
                    register[0xF] = 1
                else
                    register[0xF] = 0
                end
                register[dest_index] -= register[src_index]
        """
        if self.registers[dest_index] >= self.registers[src_index]:
            self.registers[0xF] = np.uint64(1)
        else:
            self.registers[0xF] = np.uint64(0)
        self.registers[dest_index] -= self.registers[src_index]
    
    def bitwise_right_shift(self, dest_index : int, src_value : int) -> None:
        """
        Implemements the 8XY6 opcode:
            Pseudocode:
                register[0xF] = register[dest_index] & 1
                register[dest_index] >>= (src_value + 1)
        Implementation details:
        This is a departure from the original specification as the 8XY6 opcode
        in the original specification right shifts by one only. With 64-bit
        registers, to do anything complicated there will be a fair amount of
        bloat caused by lines of single right shifts. I chose to embed the shift
        value in the opcode to prevent the need to spill registers to hold a
        value for a single instruction with the compromise that care will be
        needed to shift a value right by more than 16. src_value is incremented
        by one in the implementation as a single nibble takes values in the
        range [0, 15] but you'll never shift right by 0 as that does nothing so
        it saves code if you need to shift right by 16 precisely.
        """
        self.registers[0xF] = self.registers[dest_index] & np.uint64(1)
        self.registers[dest_index] >>= np.uint64(src_value + 1)
        
    def bitwise_left_shift(self, dest_index : int, src_value : int) -> None:
        """
        Implements the 8XYE opcode.
            Pseudocode:
                register[0xF] = register[dest_index] & (1 << 63)
                register[dest_index] <<= (src_value + 1)
        Implementation details:
        Basically see above.
        """
        self.registers[0xF] = np.uint64(
            (self.registers[dest_index] & (1 << 63)) >> 63)
        self.registers[dest_index] <<= np.uint64(src_value + 1)
    
    def skip_next_if_unequal(self, dest_index : int, src_index : int) -> None:
        """
        Implements the 9XY0 opcode.
        Skips the next instruction if register[dest_index] is equal to
        register[src_index]
        """
        if self.registers[dest_index] != self.registers[src_index]:
            self.code_ptr += 2
    
    def set_memory_ptr(self, value : int) -> None:
        """
        Implements the ANNN opcode.
        sets the memory_ptr to value.
        """
        self.memory_ptr = value
    
    def set_code_ptr_to_acc_plus_const(self, constant : int) -> None:
        """
        Implements the BNNN opcode.
        Adds registers[0] and constant and sets code_ptr to this.
        """
        self.code_ptr = self.registers[0] + constant - 2
    
    def bitwise_and_rand(self, dest_index : int, constant : int) -> None:
        """
        Implements the CXNN opcode.
        sets registers[dest_index] to randint(0, 255) & constant.
        """
        self.registers[dest_index] = np.uint64(random.randint(0, 255)) & constant
    
    def display_register_hex(self, register_index : int) -> None:
        """
        Implements the DX00 opcode.
        Prints the contents of the register_index register to the console in
        hexadecimal.
        """
        print(hex(self.registers[register_index]))
    
    def display_register_dec(self, register_index : int) -> None:
        """
        Implements the DX01 opcode.
        Prints the contents of the register_index register to the console in
        decimal.
        """
        print(self.registers[register_index])
    
    def display_register_bin(self, register_index : int) -> None:
        """
        Implements the DX02 opcode.
        Prints the contents of the register_index register to the console in
        binary.
        """
        print(bin(self.registers[value_index]))
    
    def display_register_oct(self, register_index : int) -> None:
        """
        Implements the DX03 opcode.
        Prints the contents of the register_index register to the console in
        octal.
        """
        print(oct(self.registers[register_index]))
    
    def add_register_to_memory_ptr(self, register_index : int) -> None:
        """
        Implements the EX1E opcode.
        Adds the value held in registers[register_index] to memory_ptr.
        """
        self.memory_ptr += self.registers[register_index]
    
    def spill_registers(self, register_index : int) -> None:
        """
        Implements the EX55 opcode.
        Writes the contents of registers 0 to register_index inclusive to
        the memory pointed to by memory_ptr in a big endian manner. Without
        modifying memory_ptr.
        """
        ptr = self.memory_ptr
        for register in itt.islice(self.registers, register_index):
            # reverse the list as split gives data in little endian manner and
            # we need it in a big endian format.
            tmp = c8u.split(self.registers[register_index])
            for i in range(8): # register is 8 bytes wide
                self.memory[ptr] = tmp[i]
                ptr += 1

    def load_registers(self, register_index : int) -> None:
        """
        Implements the EX65 opcode.
        Fills the registers 0 to register_index inclusive from the memory
        pointed to by memory_ptr in a big endian manner without modifying
        memory_ptr.
        """
        ptr = self.memory_ptr
        for register in range(register_index + 1):
            # 8 being the width of a register in bytes.
            tmp_bytes = [self.memory[ptr + i] for i in range(8)]
            ptr += 8
            self.registers[register] = c8u.build_int(tmp_bytes)

    
    def input_to_register_hex(self, register_index : int) -> None:
        """
        Implements the FX00 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in hexadecimal
        """
        self.registers[value_index] = np.uint64(int(input('>'), 16))
    
    def input_to_register_dec(self, register_index : int) -> None:
        """
        Implements the FX01 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in decimal
        """
        self.registers[register_index] = np.uint64(int(input('>')))
    
    def input_to_register_bin(self, register_index : int) -> None:
        """
        Implements the FX02 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in binary
        """
        self.registers[value_index] = np.uint64(int(input('>'), 2))
    
    def input_to_register_oct(self, register_index : int) -> None:
        """
        Implements the FX03 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in octal
        """
        self.registers[value_index] = np.uint64(int(input('>'), 8))
    
    def execute(self) -> None:
        """
        The main execution loop of the emulator.
        """
        while True:
            opcode = c8u.build_int([self.memory[self.code_ptr],
                self.memory[self.code_ptr + 1]])

            if opcode == 0x0000:
                return
            elif opcode == 0x01EE:
                self.subroutine_return()
            
            nib3 = c8u.get_nibble(opcode, 3)
            if nib3 == 1:
                self.goto(opcode & 0xFFF)
            elif nib3 == 2:
                self.subroutine_call(opcode & 0xFFF)
            elif nib3 == 3:
                self.skip_next_if_equal_const(c8u.get_nibble(opcode, 2),
                    c8u.low_byte(opcode))
            elif nib3 == 4:
                self.skip_next_if_unequal_const(c8u.get_nibble(opcode, 2),
                    c8u.low_byte(opcode))
            elif nib3 == 5:
                self.skip_next_if_equal(c8u.get_nibble(opcode, 2),
                    c8u.get_nibble(opcode, 1))
            elif nib3 == 6:
                self.assign_const_to_register(c8u.get_nibble(opcode, 2),
                    c8u.low_byte(opcode))
            elif nib3 == 7:
                self.add_const_to_register(c8u.get_nibble(opcode, 2),
                    c8u.low_byte(opcode))
            elif nib3 == 8:
                nib0 = c8u.get_nibble(opcode, 0)
                if nib0 == 0:
                    self.assign_register(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
                elif nib0 == 1:
                    self.bitwise_or(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
                elif nib0 == 2:
                    self.bitwise_and(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
                elif nib0 == 3:
                    self.bitwise_xor(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
                elif nib0 == 4:
                    self.add_registers(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
                elif nib0 == 5:
                    self.subtract_registers(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
                elif nib0 == 6:
                    self.bitwise_right_shift(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
                elif nib0 == 7:
                    self.subtract_registers(c8u.get_nibble(opcode, 1),
                        c8u.get_nibble(opcode, 2))
                elif nib0 == 0xE:
                    self.bitwise_left_shift(c8u.get_nibble(opcode, 2),
                        c8u.get_nibble(opcode, 1))
            elif nib3 == 9:
                self.skip_next_if_unequal(c8u.get_nibble(opcode, 2),
                    c8u.get_nibble(opcode, 1))
            elif nib3 == 0xA:
                self.set_memory_ptr(opcode & 0xFFF)
            elif nib3 == 0xB:
                self.set_code_ptr_to_acc_plus_const(opcode & 0xFFF)
            elif nib3 == 0xC:
                self.bitwise_and_rand(c8u.get_nibble(opcode, 2),
                    c8u.low_byte(opcode))
            elif nib3 == 0xD:
                nib0 = c8u.get_nibble(opcode, 0)
                if nib0 == 0:
                    self.display_register_hex(c8u.get_nibble(opcode, 2))
                elif nib0 == 1:
                    self.display_register_dec(c8u.get_nibble(opcode, 2))
                elif nib0 == 2:
                    self.display_register_bin(c8u.get_nibble(opcode, 2))
                elif nib0 == 3:
                    self.display_register_oct(c8u.get_nibble(opcode, 2))
            elif nib3 == 0xE:
                if c8u.low_byte(opcode) == 0x1E:
                    self.add_register_to_memory_ptr(c8u.get_nibble(opcode, 2))
                elif c8u.low_byte(opcode) == 0x55:
                    self.spill_registers(c8u.get_nibble(opcode, 2))
                elif c8u.low_byte(opcode) == 0x65:
                    self.load_registers(c8u.get_nibble(opcode, 2))

            elif nib3 == 0xF:
                nib0 = c8u.get_nibble(opcode, 0)
                if nib0 == 0:
                    self.input_to_register_hex(c8u.get_nibble(opcode, 2))
                elif nib0 == 1:
                    self.input_to_register_dec(c8u.get_nibble(opcode, 2))
                elif nib0 == 2:
                    self.input_to_register_bin(c8u.get_nibble(opcode, 2))
                elif nib0 == 3:
                    self.input_to_register_oct(c8u.get_nibble(opcode, 2))

            self.code_ptr += 2
            print(self.registers)
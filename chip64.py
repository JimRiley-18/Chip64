import chip64_util as c64u
import numpy as np
import itertools as itt
import warnings
import random

# Writing code to emulate low level hardware often requires using things like
# well modelled integer overflow. Numpy warns when this happens and thereby
# clogs the console with warnings about expected behaviour. This imperative
# prevents this.
warnings.filterwarnings("ignore")


class Chip64:
    """
    The main class for the chip64 emulator.
    Sound, delay and graphics are omitted for ease of implementation as I'm not
    writing games but just doing computation. I've replaced them with a few
    instructions that do numerical i/o in various formats.
    """

    def __init__(self, code=[]):
        """
        The default constructor for the class.
        """
        self.memory = [np.uint8(0) for _ in range(4096)]
        self.registers = [np.uint64(0) for _ in range(16)]
        self.stack = []
        self.code_ptr = 0
        self.memory_ptr = 0

        for i, byte in enumerate(code):
            self.memory[i] = byte

    def reset(self):
        """
        A small helper class that resets the Chip64 object, typically called in tests.
        """
        self.__init__()

    def halt(self) -> None:
        """
        Implements the 0000 opcode.
        Halts execution of the program.
        """
        c64u.program_exit()

    def subroutine_return(self) -> None:
        """
        Implements the 01EE opcode.
        Returns from the current subroutine, sets the instruction pointer to the
        address at the top of the call stack then pops the stack.
        """
        self.code_ptr = self.stack.pop()

    def goto(self, address: np.uint16) -> None:
        """
        Implements the 1NNN opcode.
        Sets the instruction pointer to address and then resumes execution.
        """
        self.code_ptr = address

    def subroutine_call(self, address: np.uint16) -> None:
        """
        Implements the 2NNN opcode.
        Calls the subroutine at address NNN.
        Pushes the code_ptr onto the call stack, then sets the code_ptr to NNN.
        """
        self.stack.append(self.code_ptr)
        self.code_ptr = address

    def skip_next_if_equal_const(
        self, register_index: np.uint16, constant: np.uint16
    ) -> None:
        """
        Implements the 3XNN opcode.
        Skips the next instruction if register[register_index] is equal to
        constant.
        """
        if self.registers[register_index] == constant:
            self.code_ptr += 2

    def skip_next_if_unequal_const(
        self, register_index: np.uint16, constant: np.uint16
    ) -> None:
        """
        Implements the 4XNN opcode.
        Skips the next instruction if register[register_index] is not equal to
        constant
        """
        if self.registers[register_index] != constant:
            self.code_ptr += 2

    def skip_next_if_equal(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implements the 5XY0 opcode.
        Skips the next instruction if register[dest_index] is equal to
        register[src_index]
        """
        if self.registers[dest_index] == self.registers[src_index]:
            self.code_ptr += 2

    def assign_const_to_register(
        self, dest_index: np.uint16, constant: np.uint16
    ) -> None:
        """
        Implements the 6XNN opcode.
        Writes constant to registers[dest_index]
        """
        self.registers[dest_index] = np.uint64(constant)

    def add_const_to_register(self, dest_index: np.uint16, constant: np.uint16) -> None:
        """
        Implements the 7XNN opcode.
        Adds byte constant to registers[dest_index] without setting the
        carry flag.
        """
        self.registers[dest_index] += np.uint64(constant)

    def assign_register(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implements the 8XY0 opcode:
            Pseudocode: register[dest_index] = register[src_index]
        """
        self.registers[dest_index] = self.registers[src_index]

    def bitwise_or(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implemements the 8XY1 opcode:
            Pseudocode: register[dest_index] |= register[src_index]
        """
        self.registers[dest_index] |= self.registers[src_index]

    def bitwise_and(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implemements the 8XY2 opcode:
            Pseudocode: register[dest_index] &= register[src_index]
        """
        self.registers[dest_index] &= self.registers[src_index]

    def bitwise_xor(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implemements the 8XY3 opcode:
            Pseudocode: register[dest_index] ^= register[src_index]
        """
        self.registers[dest_index] ^= self.registers[src_index]

    def add_registers(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implements the 8XY4 opcode.
        Adds registers X and Y together and sets carry flag if needed.
        """
        tmp = self.registers[dest_index] + self.registers[src_index]
        if tmp < self.registers[dest_index]:

            self.registers[0xF] = np.uint64(1)
        else:
            self.registers[0xF] = np.uint64(0)
        self.registers[dest_index] = np.uint64(tmp)

    def subtract_registers(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implements the 8XY5 opcode.
        Subtracts registers X and Y together and sets the flag register if
        there was no borrow.
        """
        if self.registers[dest_index] >= self.registers[src_index]:
            self.registers[0xF] = np.uint64(1)
        else:
            self.registers[0xF] = np.uint64(0)
        self.registers[dest_index] -= self.registers[src_index]

    def bitwise_right_shift(self, dest_index: np.uint16, src_value: np.uint16) -> None:
        """
        Implemements the 8XY6 opcode.
        """
        if src_value == 0:
            self.registers[0xF] = 0
            return
        # The following code assumes that src_Value > 0
        tmp = self.registers[dest_index] & np.uint64(1 << (src_value - 1))
        if tmp > 0:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0
        self.registers[dest_index] >>= np.uint64(src_value)

    def bitwise_left_shift(self, dest_index: np.uint16, src_value: np.uint16) -> None:
        """
        Implements the 8XYE opcode.
        """
        if src_value == 0:
            self.registers[0xF] = 0
            return
        tmp = self.registers[dest_index] & np.uint64(1 << (64 - src_value))
        if tmp > 0:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0
        self.registers[dest_index] <<= np.uint64(src_value)

    def skip_next_if_unequal(self, dest_index: np.uint16, src_index: np.uint16) -> None:
        """
        Implements the 9XY0 opcode.
        Skips the next instruction if register[dest_index] is equal to
        register[src_index]
        """
        if self.registers[dest_index] != self.registers[src_index]:
            self.code_ptr += 2

    def set_memory_ptr(self, value: np.uint16) -> None:
        """
        Implements the ANNN opcode.
        sets the memory_ptr to value.
        """
        self.memory_ptr = value

    def set_code_ptr_to_acc_plus_const(self, constant: np.uint16) -> None:
        """
        Implements the BNNN opcode.
        Adds registers[0] and constant and sets code_ptr to this.
        """
        self.code_ptr = self.registers[0] + constant

    def bitwise_and_rand(self, dest_index: np.uint16, constant: np.uint16) -> None:
        """
        Implements the CXNN opcode.
        sets registers[dest_index] to randint(0, 255) & constant.
        """
        self.registers[dest_index] = np.uint64(random.randint(0, 255)) & np.uint64(
            constant
        )

    def display_register_hex(self, register_index: np.uint16) -> None:
        """
        Implements the DX00 opcode.
        Prints the contents of the register_index register to the console in
        hexadecimal.
        """
        c64u.console_output(hex(self.registers[register_index]))

    def display_register_dec(self, register_index: np.uint16) -> None:
        """
        Implements the DX01 opcode.
        Prints the contents of the register_index register to the console in
        decimal.
        """
        c64u.console_output(self.registers[register_index])

    def display_register_bin(self, register_index: np.uint16) -> None:
        """
        Implements the DX02 opcode.
        Prints the contents of the register_index register to the console in
        binary.
        """
        c64u.console_output(bin(self.registers[register_index]))

    def display_register_oct(self, register_index: np.uint16) -> None:
        """
        Implements the DX03 opcode.
        Prints the contents of the register_index register to the console in
        octal.
        """
        c64u.console_output(oct(self.registers[register_index]))

    def add_register_to_memory_ptr(self, register_index: np.uint16) -> None:
        """
        Implements the EX1E opcode.
        Adds the value held in registers[register_index] to memory_ptr.
        """
        self.memory_ptr += self.registers[register_index]

    def spill_registers(self, register_index: np.uint16) -> None:
        """
        Implements the EX55 opcode.
        Writes the contents of registers 0 to register_index inclusive to
        the memory pointed to by memory_ptr in a big endian manner. Without
        modifying memory_ptr.
        """
        ptr = self.memory_ptr
        # use register_index+1 because islice iterates over range [start, stop)
        for register in itt.islice(self.registers, register_index + 1):
            tmp = c64u.split(register)
            for i in range(8):  # register is 8 bytes wide
                self.memory[ptr] = np.uint8(tmp[i])
                ptr += 1

    def load_registers(self, register_index: np.uint16) -> None:
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
            self.registers[register] = np.uint64(c64u.build_uint64(tmp_bytes))

    def input_to_register_hex(self, register_index: np.uint16) -> None:
        """
        Implements the FX00 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in hexadecimal
        """
        self.registers[register_index] = np.uint64(int(c64u.console_input(">"), 16))

    def input_to_register_dec(self, register_index: np.uint16) -> None:
        """
        Implements the FX01 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in decimal
        """
        self.registers[register_index] = np.uint64(int(c64u.console_input(">")))

    def input_to_register_bin(self, register_index: np.uint16) -> None:
        """
        Implements the FX02 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in binary
        """
        self.registers[register_index] = np.uint64(int(c64u.console_input(">"), 2))

    def input_to_register_oct(self, register_index: np.uint16) -> None:
        """
        Implements the FX03 opcode.
        Takes input from the console and places it into the register indicated
        by register_index. Input is expected in octal
        """
        self.registers[register_index] = np.uint64(int(c64u.console_input(">"), 8))

    def execute(self, num_of_cycles=None) -> None:
        """
        The main execution loop of the emulator.
        num_of_cycles gives the number of cycles you'd like the emulator to run for.
        If no parameter is passed then the emulator will cycle indefinitely.
        """
        while num_of_cycles is None or num_of_cycles > 0:
            opcode = c64u.concat(
                self.memory[self.code_ptr], self.memory[self.code_ptr + 1]
            )

            # Flag dictates if we want to increment the code ptr at the end of this iteration.
            # This prevents irritating -2 terms in code_ptr modifying instructions.
            code_ptr_increment_flag = True

            if opcode == 0x0000:
                self.halt()
            elif opcode == 0x01EE:
                self.subroutine_return()
                code_ptr_increment_flag = True

            nib3 = c64u.get_nibble(opcode, 3)
            if nib3 == 1:
                self.goto(opcode & np.uint16(0xFFF))
                code_ptr_increment_flag = False
            elif nib3 == 2:
                self.subroutine_call(opcode & np.uint16(0xFFF))
                code_ptr_increment_flag = False
            elif nib3 == 3:
                self.skip_next_if_equal_const(
                    c64u.get_nibble(opcode, 2), c64u.low_byte(opcode)
                )
            elif nib3 == 4:
                self.skip_next_if_unequal_const(
                    c64u.get_nibble(opcode, 2), c64u.low_byte(opcode)
                )
            elif nib3 == 5:
                self.skip_next_if_equal(
                    c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                )
            elif nib3 == 6:
                self.assign_const_to_register(
                    c64u.get_nibble(opcode, 2), c64u.low_byte(opcode)
                )
            elif nib3 == 7:
                self.add_const_to_register(
                    c64u.get_nibble(opcode, 2), c64u.low_byte(opcode)
                )
            elif nib3 == 8:
                nib0 = c64u.get_nibble(opcode, 0)
                if nib0 == 0:
                    self.assign_register(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
                elif nib0 == 1:
                    self.bitwise_or(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
                elif nib0 == 2:
                    self.bitwise_and(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
                elif nib0 == 3:
                    self.bitwise_xor(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
                elif nib0 == 4:
                    self.add_registers(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
                elif nib0 == 5:
                    self.subtract_registers(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
                elif nib0 == 6:
                    self.bitwise_right_shift(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
                elif nib0 == 7:
                    self.subtract_registers(
                        c64u.get_nibble(opcode, 1), c64u.get_nibble(opcode, 2)
                    )
                elif nib0 == 0xE:
                    self.bitwise_left_shift(
                        c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                    )
            elif nib3 == 9:
                self.skip_next_if_unequal(
                    c64u.get_nibble(opcode, 2), c64u.get_nibble(opcode, 1)
                )
            elif nib3 == 0xA:
                self.set_memory_ptr(opcode & np.uint16(0xFFF))
            elif nib3 == 0xB:
                self.set_code_ptr_to_acc_plus_const(opcode & np.uint16(0xFFF))
                code_ptr_increment_flag = False
            elif nib3 == 0xC:
                self.bitwise_and_rand(c64u.get_nibble(opcode, 2), c64u.low_byte(opcode))
            elif nib3 == 0xD:
                nib0 = c64u.get_nibble(opcode, 0)
                if nib0 == 0:
                    self.display_register_hex(c64u.get_nibble(opcode, 2))
                elif nib0 == 1:
                    self.display_register_dec(c64u.get_nibble(opcode, 2))
                elif nib0 == 2:
                    self.display_register_bin(c64u.get_nibble(opcode, 2))
                elif nib0 == 3:
                    self.display_register_oct(c64u.get_nibble(opcode, 2))
            elif nib3 == 0xE:
                if c64u.low_byte(opcode) == 0x1E:
                    self.add_register_to_memory_ptr(c64u.get_nibble(opcode, 2))
                elif c64u.low_byte(opcode) == 0x55:
                    self.spill_registers(c64u.get_nibble(opcode, 2))
                elif c64u.low_byte(opcode) == 0x65:
                    self.load_registers(c64u.get_nibble(opcode, 2))
            elif nib3 == 0xF:
                nib0 = c64u.get_nibble(opcode, 0)
                if nib0 == 0:
                    self.input_to_register_hex(c64u.get_nibble(opcode, 2))
                elif nib0 == 1:
                    self.input_to_register_dec(c64u.get_nibble(opcode, 2))
                elif nib0 == 2:
                    self.input_to_register_bin(c64u.get_nibble(opcode, 2))
                elif nib0 == 3:
                    self.input_to_register_oct(c64u.get_nibble(opcode, 2))

            if code_ptr_increment_flag:
                self.code_ptr += 2
            if num_of_cycles is not None:
                num_of_cycles -= 1

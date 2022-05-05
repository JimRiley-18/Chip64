import chip64
import chip64_util as c64u
import numpy as np
import unittest.mock
import random


def test_chip64_reset():
    """
    Test the chip64.reset() method, ensure that all of the member variables
    are zeroed out when this method is called.
    """
    c64 = chip64.Chip64()
    # Just fill all the member variables with guff.
    c64.memory = [np.uint8(0xFF) for _ in range(4096)]
    c64.registers = [np.uint64(0xFF) for _ in range(16)]
    c64.stack = [0xABCD, 0xABCD]
    c64.code_ptr = 0x37CB
    c64.memory_ptr = 0xFFF

    c64.reset()

    assert c64.memory == [np.uint8(0) for _ in range(4096)]
    assert c64.registers == [np.uint64(0) for _ in range(16)]
    assert c64.stack == []
    assert c64.code_ptr == 0
    assert c64.memory_ptr == 0

def test_chip64_subroutine_return():
    """
    Tests the chip64.subroutine_return() method.
    """
    c64 = chip64.Chip64()
    c64.stack.append(0x100)
    c64.subroutine_return()
    assert c64.code_ptr == 0x100
    assert c64.stack == []


def test_chip64_goto():
    """
    Test the chip64.goto() method, ensure that the code pointer is correctly modified.
    """
    c64 = chip64.Chip64()
    c64.code_ptr = 0xABC
    c64.goto(0xBCD)
    assert c64.code_ptr == 0xBCD


def test_chip64_subroutine_call():
    """
    Tests the chip64.subroutine_call() method.
    """
    c64 = chip64.Chip64()
    c64.code_ptr = 0x10
    c64.subroutine_call(0x100)
    assert c64.code_ptr == 0x100
    assert c64.stack == [0x10]


def test_chip64_skip_next_if_equal_const():
    """
    Test the chip64.skip_next_if_equal_const() method, ensure that the code pointer is correctly modified.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0xFF
    c64.skip_next_if_equal_const(0, 0xFF)
    assert c64.code_ptr == 2


def test_chip64_skip_next_if_unequal_const():
    """
    Test the chip64.skip_next_if_unequal_const() method, ensure that the code pointer is correctly modified.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0xF0
    c64.skip_next_if_unequal_const(0, 0xFF)
    assert c64.code_ptr == 2


def test_chip64_skip_next_if_equal():
    """
    Test the chip64.skip_next_if_equal() method, ensure that the code pointer is correctly modified.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 1
    c64.registers[1] = 1
    c64.skip_next_if_equal(0, 1)
    assert c64.code_ptr == 2

    c64.reset()
    c64.registers[0] = 1
    c64.registers[1] = 2
    c64.skip_next_if_equal(0, 1)
    assert c64.code_ptr != 2


def test_chip64_assign_const_to_register():
    """
    Test the chip64.assign_const_to_register() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0xFF
    c64.assign_const_to_register(0, 0xF)
    assert c64.registers[0] == 0xF


def test_chip64_add_const_to_register():
    """
    Test the chip64.add_const_to_register() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 1
    c64.add_const_to_register(0, 1)
    assert c64.registers[0] == 2


def test_chip64_assign_register():
    """
    Test the chip64.assign_register() method, ensure that the register takes the appropriate value.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0xABCDEF
    c64.assign_register(1, 0)
    assert c64.registers[1] == 0xABCDEF


def test_chip64_bitwise_or():
    """
    Test the chip64.bitwise_or() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = np.uint64(0xFFFF)
    c64.registers[1] = np.uint64(0xF0F0)
    c64.bitwise_or(0, 1)
    assert c64.registers[0] == 0xFFFF
    assert c64.registers[1] == 0xF0F0


def test_chip64_bitwise_and():
    """
    Test the chip64.bitwise_and() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = np.uint64(0xFFFF)
    c64.registers[1] = np.uint64(0xF0F0)
    c64.bitwise_and(0, 1)
    assert c64.registers[0] == 0xF0F0
    assert c64.registers[1] == 0xF0F0


def test_chip64_bitwise_xor():
    """
    Test the chip64.bitwise_xor() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = np.uint64(0xFFFF)
    c64.registers[1] = np.uint64(0xF0F0)
    c64.bitwise_xor(0, 1)
    assert c64.registers[0] == 0x0F0F
    assert c64.registers[1] == 0xF0F0


def test_chip64_add_registers():
    """
    Test the chip64.add_registers() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = np.uint64(0xAB00)
    c64.registers[1] = np.uint64(0xCD)
    c64.add_registers(0, 1)
    assert c64.registers[0] == 0xABCD
    assert c64.registers[1] == 0xCD
    assert c64.registers[0xF] == 0

    c64.reset()
    c64.registers[0] = np.uint64((1 << 64) - 1)
    c64.registers[1] = np.uint64(1)
    c64.add_registers(0, 1)
    assert c64.registers[0] == 0
    assert c64.registers[1] == 1
    assert c64.registers[0xF] == 1


def test_chip64_subtract_registers():
    """
    Test the chip64.subtract_registers() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = np.uint64(0xABCD)
    c64.registers[1] = np.uint64(0xAB00)
    c64.subtract_registers(0, 1)
    assert c64.registers[0] == 0xCD
    assert c64.registers[1] == 0xAB00
    assert c64.registers[0xF] == 1

    c64.reset()
    c64.registers[0] = np.uint64(0)
    c64.registers[1] = np.uint64(1)
    c64.subtract_registers(0, 1)
    assert c64.registers[0] == (1 << 64) - 1
    assert c64.registers[1] == 1
    assert c64.registers[0xF] == 0


def test_chip64_bitwise_right_shift():
    """
    Test the chip64.bitwise_right_shift() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = np.uint64(1)
    c64.bitwise_right_shift(0, 0)
    assert c64.registers[0] == 1
    assert c64.registers[0xF] == 0
    c64.reset()
    c64.registers[0] = np.uint64(1)
    c64.bitwise_right_shift(0, 1)
    assert c64.registers[0] == 0
    assert c64.registers[0xF] == 1
    c64.reset()
    c64.registers[0] = np.uint64(2)
    c64.bitwise_right_shift(0, 1)
    assert c64.registers[0] == 1
    assert c64.registers[0xF] == 0


def test_chip64_bitwise_left_shift():
    """
    Test the chip64.bitwise_left_shift() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = np.uint64(1)
    c64.bitwise_left_shift(0, 1)
    assert c64.registers[0] == 2
    assert c64.registers[0xF] == 0
    c64.reset()
    c64.registers[0] = np.uint64(1)
    c64.bitwise_left_shift(0, 0)
    assert c64.registers[0] == 1
    assert c64.registers[0xF] == 0
    c64.reset()
    c64.registers[0] = 0x8000000000000000
    c64.bitwise_left_shift(0, 1)
    assert c64.registers[0] == 0
    assert c64.registers[0xF] == 1


def test_chip64_skip_next_if_unequal():
    """
    Tests the c64.skip_next_if_unequal() method, ensures that the code_ptr is appropriately modified.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0
    c64.registers[1] = 1
    c64.skip_next_if_unequal(0, 1)
    assert c64.code_ptr == 2

    c64.reset()
    c64.registers[0] = 0
    c64.registers[1] = 0
    c64.skip_next_if_unequal(0, 1)
    assert c64.code_ptr != 2


def test_chip64_set_memory_ptr():
    """
    Tests the c64.set_memory_ptr() method, ensures that the memory_ptr is appropriately modified.
    """
    c64 = chip64.Chip64()
    c64.set_memory_ptr(0xDAA)
    assert c64.memory_ptr == 0xDAA


def test_chip64_set_code_ptr_to_acc_plus_const():
    """
    Tests the c64.set_code_ptr_to_acc_plus_const() method, ensures that code_ptr == registers[0] + const
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0xF
    c64.set_code_ptr_to_acc_plus_const(0xFF)
    assert c64.code_ptr == (0xF + 0xFF)


def test_chip64_bitwise_and_rand():
    """
    Tests the c64.bitwise_and_rand() method, ensures that given a seeded random number that the correct register is modified.
    """
    c64 = chip64.Chip64()
    random.seed(1)
    c64.bitwise_and_rand(0, 0xF0)
    random.seed(1)
    assert c64.registers[0] == (random.randint(0, 255) & 0xF0)


def test_chip64_display_register_hex():
    """
    Tests the c64.display_register_hex() method, ensures that the console_output method called.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0xDEADBEEF
    c64u.console_output = unittest.mock.MagicMock()
    c64.display_register_hex(0)
    assert c64u.console_output.called
    c64u.console_output.assert_called_with(hex(0xDEADBEEF))


def test_chip64_display_register_dec():
    """
    Tests the c64.display_register_dec() method, ensures that the console_output method called.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 123456789
    c64u.console_output = unittest.mock.MagicMock()
    c64.display_register_dec(0)
    assert c64u.console_output.called
    c64u.console_output.assert_called_with(str(123456789))


def test_chip64_display_register_bin():
    """
    Tests the c64.display_register_bin() method, ensures that the console_output method called.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0b1001
    c64u.console_output = unittest.mock.MagicMock()
    c64.display_register_bin(0)
    assert c64u.console_output.called
    c64u.console_output.assert_called_with(bin(0b1001))


def test_chip64_display_register_oct():
    """
    Tests the c64.display_register_oct() method, ensures that the console_output method called.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0o12345
    c64u.console_output = unittest.mock.MagicMock()
    c64.display_register_oct(0)
    assert c64u.console_output.called
    c64u.console_output.assert_called_with(oct(0o12345))


def test_chip64_add_register_to_memory_ptr():
    """
    Tests that the c64.add_register_to_memory_ptr() method, ensures that the memory_ptr is modified correctly.
    """
    c64 = chip64.Chip64()
    c64.memory_ptr = 0x100
    c64.registers[0] = 0xAB
    c64.add_register_to_memory_ptr(0)
    assert c64.memory_ptr == 0x1AB


def test_chip64_spill_registers():
    """
    Tests the c64.spill_registers() method.
    """
    c64 = chip64.Chip64()
    c64.registers[0] = 0xABCD686
    c64.registers[1] = 0xCDEF123
    c64.memory_ptr = 0xFF
    c64.spill_registers(1)
    # It is important to make sure that memory_ptr is unchanged first because
    # the rest of the test depends on this.
    assert c64.memory_ptr == 0xFF
    dump1 = c64u.build_uint64([c64.memory[c64.memory_ptr + i] for i in range(8)])
    dump2 = c64u.build_uint64([c64.memory[c64.memory_ptr + 8 + i] for i in range(8)])
    assert np.uint64(dump1) == c64.registers[0]
    assert np.uint64(dump2) == c64.registers[1]


def test_chip64_load_registers():
    """
    Tests the c64.load_registers() method.
    """
    c64 = chip64.Chip64()
    c64.memory_ptr = 0x24

    tmp1 = [0xAB, 0xCD, 0x1E, 0x44, 0xF9, 0xD1, 0xCC, 0x22]
    tmp2 = [0xFB, 0x19, 0x57, 0xA2, 0xC4, 0xC2, 0xDE, 0x55]

    # load the two byte arrays into memory
    for i in range(8):
        c64.memory[0x24 + i] = np.uint8(tmp1[i])
    for i in range(8):
        c64.memory[0x24 + 8 + i] = np.uint8(tmp2[i])

    c64.load_registers(1)
    assert c64.registers[0] == 0xABCD1E44F9D1CC22
    assert c64.registers[1] == 0xFB1957A2C4C2DE55
    assert c64.memory_ptr == 0x24


def test_chip64_input_register_hex():
    """
    Tests the c64.input_register_hex() method.
    """
    c64 = chip64.Chip64()
    c64u.console_input = unittest.mock.MagicMock(return_value=hex(0x1234))
    c64.input_to_register_hex(0)
    assert c64.registers[0] == 0x1234


def test_chip64_input_register_dec():
    """
    Tests the c64.input_register_dec() method.
    """
    c64 = chip64.Chip64()
    c64u.console_input = unittest.mock.MagicMock(return_value=123456)
    c64.input_to_register_dec(0)
    assert c64.registers[0] == 123456


def test_chip64_input_register_bin():
    """
    Tests the c64.input_register_bin() method.
    """
    c64 = chip64.Chip64()
    c64u.console_input = unittest.mock.MagicMock(return_value=bin(0b1001))
    c64.input_to_register_bin(0)
    assert c64.registers[0] == 0b1001


def test_chip64_input_register_oct():
    """
    Tests the c64.input_register_oct() method.
    """
    c64 = chip64.Chip64()
    c64u.console_input = unittest.mock.MagicMock(return_value=oct(0o1771))
    c64.input_to_register_oct(0)
    assert c64.registers[0] == 0o1771

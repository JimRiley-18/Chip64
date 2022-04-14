import chip8 as c8
import chip8_util as c8u
import numpy as np
import unittest.mock
import random

def test_chip8_reset():
    """
    Test the Chip8.reset() method, ensure that all of the member variables
    are zeroed out when this method is called.
    """
    chip8 = c8.Chip8()
    # Just fill all the member variables with guff.
    chip8.memory = [np.uint8(0xFF) for _ in range(4096)]
    chip8.registers = [np.uint64(0xFF) for _ in range(16)]
    chip8.stack = [0xABCD, 0XABCD]
    chip8.code_ptr = 0x37CB
    chip8.memory_ptr = 0xFFF

    chip8.reset()

    assert chip8.memory == [np.uint8(0) for _ in range(4096)]
    assert chip8.registers == [np.uint64(0) for _ in range(16)]
    assert chip8.stack == []
    assert chip8.code_ptr == 0
    assert chip8.memory_ptr == 0

def test_chip8_halt():
    """
    Tests the chip8.halt() Method.
    This test does so by looking for the SystemExit exception I throw then returning,
    if SystemExit is not thrown then I simply assert False and the test fails.
    """
    chip8 = c8.Chip8()
    try:
        chip8.halt()
    except SystemExit:
        assert True
    else:
        assert False

def test_chip8_subroutine_return():
    """
    Tests the chip8.subroutine_return() method.
    """
    chip8 = c8.Chip8()
    chip8.stack.append(0x100)
    chip8.subroutine_return()
    assert chip8.code_ptr == 0x100
    assert chip8.stack == []

def test_chip8_goto():
    """
    Test the chip8.goto() method, ensure that the code pointer is correctly modified.
    """
    chip8 = c8.Chip8()
    chip8.code_ptr = 0xABC
    chip8.goto(0xBCD)
    assert chip8.code_ptr == 0xBCD

def test_chip8_subroutine_call():
    """
    Tests the chip8.subroutine_call() method.
    """
    chip8 = c8.Chip8()
    chip8.code_ptr = 0x10
    chip8.subroutine_call(0x100)
    assert chip8.code_ptr == 0x100
    assert chip8.stack == [0x10]

def test_chip8_skip_next_if_equal_const():
    """
    Test the chip8.skip_next_if_equal_const() method, ensure that the code pointer is correctly modified.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0xFF
    chip8.skip_next_if_equal_const(0, 0xFF)
    assert chip8.code_ptr == 2

def test_chip8_skip_next_if_unequal_const():
    """
    Test the chip8.skip_next_if_unequal_const() method, ensure that the code pointer is correctly modified.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0xF0
    chip8.skip_next_if_unequal_const(0, 0xFF)
    assert chip8.code_ptr == 2

def test_chip8_skip_next_if_equal():
    """
    Test the chip8.skip_next_if_equal() method, ensure that the code pointer is correctly modified.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 1
    chip8.registers[1] = 1
    chip8.skip_next_if_equal(0, 1)
    assert chip8.code_ptr == 2

    chip8.reset()
    chip8.registers[0] = 1
    chip8.registers[1] = 2
    chip8.skip_next_if_equal(0, 1)
    assert chip8.code_ptr != 2

def test_chip8_assign_const_to_register():
    """
    Test the chip8.assign_const_to_register() method.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0xFF
    chip8.assign_const_to_register(0, 0xF)
    assert chip8.registers[0] == 0xF

def test_chip8_add_const_to_register():
    """
    Test the chip8.add_const_to_register() method.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 1
    chip8.add_const_to_register(0, 1)
    assert chip8.registers[0] == 2

def test_chip8_assign_register():
    """
    Test the chip8.assign_register() method, ensure that the register takes the appropriate value.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0xABCDEF
    chip8.assign_register(1, 0)
    assert chip8.registers[1] == 0xABCDEF

def test_chip8_bitwise_or():
    chip8 = c8.Chip8()
    chip8.registers[0] = np.uint64(0xFFFF)
    chip8.registers[1] = np.uint64(0xF0F0)
    chip8.bitwise_or(0, 1)
    assert chip8.registers[0] == 0xFFFF
    assert chip8.registers[1] == 0xF0F0

def test_chip8_bitwise_and():
    chip8 = c8.Chip8()
    chip8.registers[0] = np.uint64(0xFFFF)
    chip8.registers[1] = np.uint64(0xF0F0)
    chip8.bitwise_and(0, 1)
    assert chip8.registers[0] == 0xF0F0
    assert chip8.registers[1] == 0xF0F0

def test_chip8_bitwise_xor():
    chip8 = c8.Chip8()
    chip8.registers[0] = np.uint64(0xFFFF)
    chip8.registers[1] = np.uint64(0xF0F0)
    chip8.bitwise_xor(0, 1)
    assert chip8.registers[0] == 0x0F0F
    assert chip8.registers[1] == 0xF0F0


def test_chip8_add_registers():
    chip8 = c8.Chip8()
    chip8.registers[0] = np.uint64(0xAB00)
    chip8.registers[1] = np.uint64(0xCD)
    chip8.add_registers(0, 1)
    assert chip8.registers[0] == 0xABCD
    assert chip8.registers[1] == 0xCD
    assert chip8.registers[0xF] == 0

    chip8.reset()
    chip8.registers[0] = np.uint64((1 << 64) - 1)
    chip8.registers[1] = np.uint64(1)
    chip8.add_registers(0, 1)
    assert chip8.registers[0] == 0
    assert chip8.registers[1] == 1
    assert chip8.registers[0xF] == 1


def test_chip8_subtract_registers():
    chip8 = c8.Chip8()
    chip8.registers[0] = np.uint64(0xABCD)
    chip8.registers[1] = np.uint64(0xAB00)
    chip8.subtract_registers(0, 1)
    assert chip8.registers[0] == 0xCD
    assert chip8.registers[1] == 0xAB00
    assert chip8.registers[0xF] == 1

    chip8.reset()
    chip8.registers[0] = np.uint64(0)
    chip8.registers[1] = np.uint64(1)
    chip8.subtract_registers(0, 1)
    assert chip8.registers[0] == (1 << 64) - 1
    assert chip8.registers[1] == 1
    assert chip8.registers[0xF] == 0

def test_chip8_skip_next_if_unequal():
    """
    Tests the chip8.skip_next_if_unequal() method, ensures that the code_ptr is appropriately modified.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0
    chip8.registers[1] = 1
    chip8.skip_next_if_unequal(0, 1)
    assert chip8.code_ptr == 2

    chip8.reset()
    chip8.registers[0] = 0
    chip8.registers[1] = 0
    chip8.skip_next_if_unequal(0, 1)
    assert chip8.code_ptr != 2

def test_chip8_set_memory_ptr():
    """
    Tests the chip8.set_memory_ptr() method, ensures that the memory_ptr is appropriately modified.
    """
    chip8 = c8.Chip8()
    chip8.set_memory_ptr(0xDAA)
    assert chip8.memory_ptr == 0xDAA

def test_chip8_set_code_ptr_to_acc_plus_const():
    """
    Tests the chip8.set_code_ptr_to_acc_plus_const() method, ensures that code_ptr == registers[0] + const
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0xF
    chip8.set_code_ptr_to_acc_plus_const(0xFF)
    assert chip8.code_ptr == (0xF + 0xFF)

def test_chip8_bitwise_and_rand():
    """
    Tests the chip8.bitwise_and_rand() method, ensures that given a seeded random number that the correct register is modified.
    """
    chip8 = c8.Chip8()
    random.seed(1)
    chip8.bitwise_and_rand(0, 0xF0)
    random.seed(1)
    assert chip8.registers[0] == (random.randint(0, 255) & 0xF0)

def test_chip8_display_register_hex():
    """
    Tests the chip8.display_register_hex() method, ensures that the console_output method called.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0xDEADBEEF
    c8u.console_output = unittest.mock.MagicMock()
    chip8.display_register_hex(0)
    assert c8u.console_output.called
    c8u.console_output.assert_called_with(hex(0xDEADBEEF))

def test_chip8_display_register_dec():
    """
    Tests the chip8.display_register_dec() method, ensures that the console_output method called.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 123456789
    c8u.console_output = unittest.mock.MagicMock()
    chip8.display_register_dec(0)
    assert c8u.console_output.called
    c8u.console_output.assert_called_with(123456789)

def test_chip8_display_register_bin():
    """
    Tests the chip8.display_register_bin() method, ensures that the console_output method called.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0b1001
    c8u.console_output = unittest.mock.MagicMock()
    chip8.display_register_bin(0)
    assert c8u.console_output.called
    c8u.console_output.assert_called_with(bin(0b1001))

def test_chip8_display_register_oct():
    """
    Tests the chip8.display_register_oct() method, ensures that the console_output method called.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0o12345
    c8u.console_output = unittest.mock.MagicMock()
    chip8.display_register_oct(0)
    assert c8u.console_output.called
    c8u.console_output.assert_called_with(oct(0o12345))

def test_chip8_add_register_to_memory_ptr():
    """
    Tests that the chip8.add_register_to_memory_ptr() method, ensures that the memory_ptr is modified correctly.
    """
    chip8 = c8.Chip8()
    chip8.memory_ptr = 0x100
    chip8.registers[0] = 0xAB
    chip8.add_register_to_memory_ptr(0)
    assert chip8.memory_ptr == 0x1AB

def test_chip8_spill_registers():
    """
    Tests the chip8.spill_registers() method.
    """
    chip8 = c8.Chip8()
    chip8.registers[0] = 0xABCD686
    chip8.registers[1] = 0xCDEF123
    chip8.memory_ptr = 0xFF
    chip8.spill_registers(1)
    # It is important to make sure that memory_ptr is unchanged first because
    # the rest of the test depends on this.
    assert chip8.memory_ptr == 0xFF
    dump1 = c8u.build_uint64([chip8.memory[chip8.memory_ptr + i] for i in range(8)])
    dump2 = c8u.build_uint64([chip8.memory[chip8.memory_ptr+8 + i] for i in range(8)])
    assert np.uint64(dump1) == chip8.registers[0]
    assert np.uint64(dump2) == chip8.registers[1]

def test_chip8_load_registers():
    """
    Tests the chip8.load_registers() method.
    """
    chip8 = c8.Chip8()
    chip8.memory_ptr = 0x24

    tmp1 = [0xAB, 0xCD, 0x1E, 0x44, 0xF9, 0xD1, 0xCC, 0x22]
    tmp2 = [0xFB, 0x19, 0x57, 0xA2, 0xC4, 0xC2, 0xDE, 0x55]

    # load the two byte arrays into memory
    for i in range(8):
        chip8.memory[0x24 + i] = np.uint8(tmp1[i])
    for i in range(8):
        chip8.memory[0x24 + 8 + i] = np.uint8(tmp2[i])
    
    chip8.load_registers(1)
    assert chip8.registers[0] == 0xABCD1E44F9D1CC22
    assert chip8.registers[1] == 0xFB1957A2C4C2DE55

def test_chip8_input_register_hex():
    """
    Tests the chip8.input_register_hex() method.
    """
    chip8 = c8.Chip8()
    c8u.console_input = unittest.mock.MagicMock(return_value=hex(0x1234))
    chip8.input_to_register_hex(0)
    assert chip8.registers[0] == 0x1234

def test_chip8_input_register_dec():
    """
    Tests the chip8.input_register_dec() method.
    """
    chip8 = c8.Chip8()
    c8u.console_input = unittest.mock.MagicMock(return_value=123456)
    chip8.input_to_register_dec(0)
    assert chip8.registers[0] == 123456

def test_chip8_input_register_bin():
    """
    Tests the chip8.input_register_bin() method.
    """
    chip8 = c8.Chip8()
    c8u.console_input = unittest.mock.MagicMock(return_value=bin(0b1001))
    chip8.input_to_register_bin(0)
    assert chip8.registers[0] == 0b1001

def test_chip8_input_register_oct():
    """
    Tests the chip8.input_register_oct() method.
    """
    chip8 = c8.Chip8()
    c8u.console_input = unittest.mock.MagicMock(return_value=oct(0o1771))
    chip8.input_to_register_oct(0)
    assert chip8.registers[0] == 0o1771
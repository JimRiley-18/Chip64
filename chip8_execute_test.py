import chip8 as c8
import unittest.mock

def test_chip8_execute_HALT():
    """
    Tests that the chip8.execute() calls halt when a halt opcode is passed.
    """
    code = [0, 0]
    chip8 = c8.Chip8(code)
    chip8.halt = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.halt.called

def test_chip8_execute_RET():
    """
    Tests that the chip8.execute() method calls subroutine_return when a RET code is passed.
    """
    code = [0x01, 0xEE]
    chip8 = c8.Chip8(code)
    chip8.subroutine_return = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.subroutine_return.called

def test_chip8_execute_CALL():
    """
    Tests that the chip8.execute() method calls subroutine_call when a CALL code is passed.
    """
    code = [0x20, 0x2]
    chip8 = c8.Chip8(code)
    chip8.subroutine_call = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.subroutine_call.called

def test_chip8_execute_GOTO():
    """
    Tests that the chip8.execute() method calls goto with the correct address
    when a GOTO opcode is passed.
    """
    code = [0x1A, 0XBC]
    chip8 = c8.Chip8(code)
    chip8.goto = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.goto.called
    chip8.goto.assert_called_with(0xABC)

def test_chip8_execute_SNEC():
    """
    Tests that the chip8.execute() method calls skip_next_if_equal_const with the correct parameters
    when a SNEC opcode is passed.
    """
    code = [0x30, 0xFF]
    chip8 = c8.Chip8(code)
    chip8.skip_next_if_equal_const = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.skip_next_if_equal_const.called
    chip8.skip_next_if_equal_const.assert_called_with(0, 0xFF)

def test_chip8_execute_SNUEC():
    """
    Tests that the chip8.execute() method calls skip_next_if_unequal_const with the correct parameters
    when a SNUEC opcode is passed.
    """
    code = [0x40, 0xFF]
    chip8 = c8.Chip8(code)
    chip8.skip_next_if_unequal_const = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.skip_next_if_unequal_const.called
    chip8.skip_next_if_unequal_const.assert_called_with(0, 0xFF)

def test_chip8_execute_SNE():
    """
    Tests that the chip8.execute() method calls skip_next_if_equal with the correct parameters when a SNE opcode
    is passed.
    """
    code = [0x50, 0x10]
    chip8 = c8.Chip8(code)
    chip8.skip_next_if_equal = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.skip_next_if_equal.called
    chip8.skip_next_if_equal.assert_called_with(0, 1)

def test_chip8_execute_ACR():
    """
    Tests that the chip8.execute() method calls assign_const_to_register with the correct parameters when a ACR opcode
    is passed.
    """
    code = [0x62, 0xCD]
    chip8 = c8.Chip8(code)
    chip8.assign_const_to_register = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.assign_const_to_register.called
    chip8.assign_const_to_register.assert_called_with(2, 0xCD)

def test_chip8_execute_ADCR():
    """
    Tests that the chip8.execute() method calls add_const_to_register with the correct parameters when a ADCR opcode is passed.
    """
    code = [0x7F, 0xD9]
    chip8 = c8.Chip8(code)
    chip8.add_const_to_register = unittest.mock.MagicMock()
    chip8.execute(num_of_cycles=1)
    assert chip8.add_const_to_register.called
    chip8.add_const_to_register.assert_called_with(0xF, 0xD9)


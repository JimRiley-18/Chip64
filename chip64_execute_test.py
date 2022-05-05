import chip64 as chip64
import unittest.mock


def test_chip64_execute_RET():
    """
    Tests that the chip64.execute() method calls subroutine_return when a RET code is passed.
    """
    code = [0x01, 0xEE]
    c64 = chip64.Chip64(code)
    c64.subroutine_return = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.subroutine_return.called


def test_chip64_execute_CALL():
    """
    Tests that the chip64.execute() method calls subroutine_call when a CALL code is passed.
    """
    code = [0x20, 0x2]
    c64 = chip64.Chip64(code)
    c64.subroutine_call = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.subroutine_call.called
    c64.subroutine_call.assert_called_with(0x2)


def test_chip64_execute_GOTO():
    """
    Tests that the chip64.execute() method calls goto with the correct address
    when a GOTO opcode is passed.
    """
    code = [0x1A, 0xBC]
    c64 = chip64.Chip64(code)
    c64.goto = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.goto.called
    c64.goto.assert_called_with(0xABC)


def test_chip64_execute_SNEC():
    """
    Tests that the chip64.execute() method calls skip_next_if_equal_const with the correct parameters
    when a SNEC opcode is passed.
    """
    code = [0x30, 0xFF]
    c64 = chip64.Chip64(code)
    c64.skip_next_if_equal_const = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.skip_next_if_equal_const.called
    c64.skip_next_if_equal_const.assert_called_with(0, 0xFF)


def test_chip64_execute_SNUEC():
    """
    Tests that the chip64.execute() method calls skip_next_if_unequal_const with the correct parameters
    when a SNUEC opcode is passed.
    """
    code = [0x40, 0xFF]
    c64 = chip64.Chip64(code)
    c64.skip_next_if_unequal_const = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.skip_next_if_unequal_const.called
    c64.skip_next_if_unequal_const.assert_called_with(0, 0xFF)


def test_chip64_execute_SNE():
    """
    Tests that the chip64.execute() method calls skip_next_if_equal with the correct parameters when a SNE opcode
    is passed.
    """
    code = [0x50, 0x10]
    c64 = chip64.Chip64(code)
    c64.skip_next_if_equal = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.skip_next_if_equal.called
    c64.skip_next_if_equal.assert_called_with(0, 1)


def test_chip64_execute_ACR():
    """
    Tests that the chip64.execute() method calls assign_const_to_register with the correct parameters when a ACR opcode
    is passed.
    """
    code = [0x62, 0xCD]
    c64 = chip64.Chip64(code)
    c64.assign_const_to_register = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.assign_const_to_register.called
    c64.assign_const_to_register.assert_called_with(2, 0xCD)


def test_chip64_execute_ADCR():
    """
    Tests that the chip64.execute() method calls add_const_to_register with the correct parameters when a ADCR opcode is passed.
    """
    code = [0x7F, 0xD9]
    c64 = chip64.Chip64(code)
    c64.add_const_to_register = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.add_const_to_register.called
    c64.add_const_to_register.assert_called_with(0xF, 0xD9)


def test_chip64_execute_AR():
    """
    Tests that the chip64.execute() method calls assign_register with the correct parameters when a AR opcode is passed.
    """
    code = [0x84, 0x70]
    c64 = chip64.Chip64(code)
    c64.assign_register = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.assign_register.called
    c64.assign_register.assert_called_with(0x4, 0x7)


def test_chip64_execute_OR():
    """
    Tests that the chip64.execute() method calls bitwise_or with the correct parameters when a OR opcode is passed.
    """
    code = [0x8F, 0x21]
    c64 = chip64.Chip64(code)
    c64.bitwise_or = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.bitwise_or.called
    c64.bitwise_or.assert_called_with(0xF, 0x2)


def test_chip64_execute_AND():
    """
    Tests that the chip64.execute() method calls bitwise_and with the correct parameters when a OR opcode is passed.
    """
    code = [0x81, 0xE2]
    c64 = chip64.Chip64(code)
    c64.bitwise_and = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.bitwise_and.called
    c64.bitwise_and.assert_called_with(0x1, 0xE)


def test_chip64_execute_XOR():
    """
    Tests that the chip64.execute() method calls bitwise_xor with the correct parameters when a XOR opcode is passed.
    """
    code = [0x80, 0x03]
    c64 = chip64.Chip64(code)
    c64.bitwise_xor = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.bitwise_xor.called
    c64.bitwise_xor.assert_called_with(0x0, 0x0)


def test_chip64_execute_ADD():
    """
    Tests that the chip64.execute() method calls bitwise_xor with the correct parameters when a ADD opcode is passed.
    """
    code = [0x8A, 0x74]
    c64 = chip64.Chip64(code)
    c64.add_registers = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.add_registers.called
    c64.add_registers.assert_called_with(0xA, 0x7)


def test_chip64_execute_SUB():
    """
    Tests that the chip64.execute() method calls subtract_registers with the correct parameters when a SUB opcode is passed.
    """
    code = [0x80, 0xB5]
    c64 = chip64.Chip64(code)
    c64.subtract_registers = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.subtract_registers.called
    c64.subtract_registers.assert_called_with(0x0, 0xB)


def test_chip64_execute_SHR():
    """
    Tests that the chip64.execute() method calls bitwise_right_shift with the correct parameters when a SHR opcode is passed.
    """
    code = [0x8F, 0x46]
    c64 = chip64.Chip64(code)
    c64.bitwise_right_shift = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.bitwise_right_shift.called
    c64.bitwise_right_shift.assert_called_with(0xF, 0x4)


def test_chip64_execute_RSUB():
    """
    Tests that the chip64.execute() method calls bitwise_xor with the correct parameters when a RSUB opcode is passed.
    """
    code = [0x86, 0x17]
    c64 = chip64.Chip64(code)
    c64.subtract_registers = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.subtract_registers.called
    c64.subtract_registers.assert_called_with(0x1, 0x6)


def test_chip64_execute_SHL():
    """
    Tests that the chip64.execute() method calls bitwise_left_shift with the correct parameters when a SHL opcode is passed.
    """
    code = [0x82, 0x3E]
    c64 = chip64.Chip64(code)
    c64.bitwise_left_shift = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.bitwise_left_shift.called
    c64.bitwise_left_shift.assert_called_with(0x2, 0x3)


def test_chip64_execute_SNUE():
    """
    Tests that the chip64.execute() method calls skip_next_if_unequal with the correct parameters when a SNUE opcode is passed.
    """
    code = [0x9A, 0x40]
    c64 = chip64.Chip64(code)
    c64.skip_next_if_unequal = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.skip_next_if_unequal.called
    c64.skip_next_if_unequal.assert_called_with(0xA, 0x4)


def test_chip64_execute_SMP():
    """
    Tests that the chip64.execute() method calls set_memory_ptr with the correct parameters when a SMP opcode is passed.
    """
    code = [0xAB, 0xCE]
    c64 = chip64.Chip64(code)
    c64.set_memory_ptr = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.set_memory_ptr.called
    c64.set_memory_ptr.assert_called_with(0xBCE)

    code = [0xA0, 0x02]
    c64 = chip64.Chip64(code)
    c64.set_memory_ptr = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.set_memory_ptr.called
    c64.set_memory_ptr.assert_called_with(0x2)


def test_chip64_execute_CPAC():
    """
    Tests that the chip64.execute() method calls set_code_ptr_to_acc_plus_const with the correct parameters when a
    CPAC opcode is passed.
    """
    code = [0xBC, 0x12]
    c64 = chip64.Chip64(code)
    c64.set_code_ptr_to_acc_plus_const = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.set_code_ptr_to_acc_plus_const.called
    c64.set_code_ptr_to_acc_plus_const.assert_called_with(0xC12)


def test_chip64_execute_BAR():
    """
    Tests that the chip64.execute() method calls bitwise_and_rand with the correct parameters when a BAR opcode is passed.
    """
    code = [0xC5, 0x23]
    c64 = chip64.Chip64(code)
    c64.bitwise_and_rand = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.bitwise_and_rand.called
    c64.bitwise_and_rand.assert_called_with(0x5, 0x23)


def test_chip64_execute_DRH():
    """
    Tests that the chip64.execute() method calls display_register_hex with the correct parameters when a DRH opcode is passed.
    """
    code = [0xD3, 0]
    c64 = chip64.Chip64(code)
    c64.display_register_hex = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.display_register_hex.called
    c64.display_register_hex.assert_called_with(0x3)


def test_chip64_execute_DRD():
    """
    Tests that the chip64.execute() method calls display_register_dec with the correct parameters when a DRD opcode is passed.
    """
    code = [0xD2, 1]
    c64 = chip64.Chip64(code)
    c64.display_register_dec = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.display_register_dec.called
    c64.display_register_dec.assert_called_with(0x2)


def test_chip64_execute_DRB():
    """
    Tests that the chip64.execute() method calls display_register_bin with the correct parameters when a DRB opcode is passed.
    """
    code = [0xDF, 2]
    c64 = chip64.Chip64(code)
    c64.display_register_bin = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.display_register_bin.called
    c64.display_register_bin.assert_called_with(0xF)


def test_chip64_execute_DRO():
    """
    Tests that the chip64.execute() method calls display_register_oct with the correct parameters when a DRO opcode is passed.
    """
    code = [0xDD, 3]
    c64 = chip64.Chip64(code)
    c64.display_register_oct = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.display_register_oct.called
    c64.display_register_oct.assert_called_with(0xD)


def test_chip64_execute_MPAR():
    """
    Tests that the chip64.execute() method calls add_register_to_memory_ptr with the correct parameters when a MPAR opcode is passed.
    """
    code = [0xE8, 0x1E]
    c64 = chip64.Chip64(code)
    c64.add_register_to_memory_ptr = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.add_register_to_memory_ptr.called
    c64.add_register_to_memory_ptr.assert_called_with(0x8)


def test_chip64_execute_SPILL():
    """
    Tests that the chip64.execute() method calls spill_registers with the correct parameters when a SPILL opcode is passed.
    """
    code = [0xE7, 0x55]
    c64 = chip64.Chip64(code)
    c64.spill_registers = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.spill_registers.called
    c64.spill_registers.assert_called_with(0x7)


def test_chip64_execute_LOAD():
    """
    Tests that the chip64.execute() method calls load_registers with the correct parameters when a LOAD opcode is passed.
    """
    code = [0xE2, 0x65]
    c64 = chip64.Chip64(code)
    c64.load_registers = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.load_registers.called
    c64.load_registers.assert_called_with(0x2)


def test_chip64_execute_IRH():
    """
    Tests that the chip64.execute() method calls input_register_hex with the correct parameters when a IRH opcode is passed.
    """
    code = [0xF3, 0]
    c64 = chip64.Chip64(code)
    c64.input_to_register_hex = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.input_to_register_hex.called
    c64.input_to_register_hex.assert_called_with(0x3)


def test_chip64_execute_IRD():
    """
    Tests that the chip64.execute() method calls input_register_dec with the correct parameters when a IRD opcode is passed.
    """
    code = [0xF3, 1]
    c64 = chip64.Chip64(code)
    c64.input_to_register_dec = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.input_to_register_dec.called
    c64.input_to_register_dec.assert_called_with(0x3)


def test_chip64_execute_IRB():
    """
    Tests that the chip64.execute() method calls input_register_bin with the correct parameters when a IRB opcode is passed.
    """
    code = [0xF3, 2]
    c64 = chip64.Chip64(code)
    c64.input_to_register_bin = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.input_to_register_bin.called
    c64.input_to_register_bin.assert_called_with(0x3)


def test_chip64_execute_IRO():
    """
    Tests that the chip64.execute() method calls input_register_oct with the correct parameters when a IRO opcode is passed.
    """
    code = [0xF3, 3]
    c64 = chip64.Chip64(code)
    c64.input_to_register_oct = unittest.mock.MagicMock()
    c64.execute(num_of_cycles=1)
    assert c64.input_to_register_oct.called
    c64.input_to_register_oct.assert_called_with(0x3)

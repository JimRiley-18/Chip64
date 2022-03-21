import chip8 as c8
import numpy as np

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

def test_chip8_bitwise_left_shift():
    chip8 = c8.Chip8()
    chip8.registers[0] = np.uint64((1 << 64) - 1)
    chip8.bitwise_left_shift(0, 3)
    assert chip8.registers[0] == np.uint64(0xFFFFFFFFFFFFFFF8)
    assert chip8.registers[0xF] == 0x7
    chip8.reset()
    chip8.registers[0] = np.uint64(0xF)
    chip8.bitwise_left_shift(0, 4)
    assert chip8.registers[0] == np.uint64(0xF0)
    assert chip8.registers[0xF] == 0
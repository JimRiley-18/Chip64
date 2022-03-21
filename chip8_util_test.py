import chip8_util as c8u
import numpy as np


def test_high_byte():
    assert c8u.high_byte(np.uint16(0xABCD)) == 0xAB


def test_low_byte():
    assert c8u.low_byte(np.uint16(0xABCD)) == 0xCD


def test_concat():
    assert c8u.concat(0xAB, 0xCD) == 0xABCD


def test_get_nibble():
    assert c8u.get_nibble(0xABCD, 0) == 0xD


def test_is_hex():
    assert c8u.is_hex("0xABCD") == True
    assert c8u.is_hex("zf") == False


def test_split():
    assert c8u.split(0xABCDEF12) == [0xAB, 0xCD, 0xEF, 0x12]


def test_build_int():
    assert c8u.build_int([0xAB, 0xCD, 0xEF, 0x12]) == 0xABCDEF12

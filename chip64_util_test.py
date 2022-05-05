import chip64_util as c64u
import numpy as np


def test_high_byte():
    """
    Test the high_byte() util function.
    """
    assert c64u.high_byte(np.uint16(0xABCD)) == 0xAB


def test_low_byte():
    """
    Test the low_byte() util function.
    """
    assert c64u.low_byte(np.uint16(0xABCD)) == 0xCD


def test_concat():
    """
    Test the concat() util function.
    """
    assert c64u.concat(0xAB, 0xCD) == 0xABCD


def test_get_nibble():
    """
    Test the get_nibble() util function.
    """
    assert c64u.get_nibble(0xABCD, 0) == 0xD


def test_is_hex():
    """
    Test the is_hex() util function.
    """
    assert c64u.is_hex("0xABCD") == True
    assert c64u.is_hex("zf") == False


def test_split():
    """
    Test the split() util function.
    """
    assert c64u.split(0xABCDEF123456789A) == [
        0xAB,
        0xCD,
        0xEF,
        0x12,
        0x34,
        0x56,
        0x78,
        0x9A,
    ]


def test_build_uint64():
    """
    Test the build_uint64() util function.
    """
    assert c64u.build_uint64([0, 0, 0, 0, 0xAB, 0xCD, 0xEF, 0x12]) == 0xABCDEF12
    assert c64u.build_uint64([0x0, 0x0, 0x0, 0x0, 0x0, 0x3d, 0x09, 0x0]) == 0x3D0900
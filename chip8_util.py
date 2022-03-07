"""
A library for useful functions that it doesn't make sense to include in the
main emulator directory.
"""

import numpy as np

def high_byte(value : np.uint16) -> np.uint8:
    """
    Given a 16 bit value 0xABCD, returns 0xAB.
    """
    return (value & 0xFF) >> 8

def low_byte(value : np.uint16) -> np.uint8:
    """
    Given a 16 bit value 0xABCD, returns 0xCD.
    """
    return np.uint8(value & 0xFF)

def concat(hb : np.uint8, lb : np.uint8) -> np.uint16:
    """
    Concatenates a high byte (hb) and a low byte (lb) into a word.
    """
    return np.uint16((hb << 8) | lb)

def get_nibble(value : int, n : int) -> int:
    """
    Returns the nth nibble of a number.
    example: get_nibble(0xABCD, 0) = 0xD
    """
    return (value & (0xF << (4*n))) >> (4*n)

def is_hex(string : str) -> bool:
    """
    Checks if a string is hexadecimal, returns true if so and false otherwise.
    """
    try:
        int(string, 16)
        return True
    except ValueError:
        return False

def split(value : int) -> list:
    """
    Splits a numerical value into it's composite bytes and returns them in a
    big endian manner.
    """
    rv = []
    while value > 0:
        rv.append(value & 0xFF)
        value >>= 8
    return reversed(rv)

def build_int(byte_list : list) -> int:
    """
    Builds an int from a list of bytes.
    """
    rv = 0
    for byte in byte_list:
        rv = (rv << 8) | byte
    return rv

def strip_non_numeric_words(code : list) -> list:
    """
    Returns a list of all the hexadecimal numbers in the list as i
    """
    return [np.uint16(int(word, 16)) for word in code if is_hex(word)]
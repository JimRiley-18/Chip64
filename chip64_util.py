"""
A library for useful functions that it doesn't make sense to include in the
main emulator directory.
"""

import numpy as np
import sys


def high_byte(value: np.uint16) -> np.uint16:
    """
    Given a 16 bit value 0xABCD, returns 0xAB.
    """
    return np.uint16((value & 0xFF00) >> 8)


def low_byte(value: np.uint16) -> np.uint16:
    """
    Given a 16 bit value 0xABCD, returns 0xCD.
    """
    return np.uint16(value & 0xFF)


def concat(hb: np.uint8, lb: np.uint8) -> np.uint16:
    """
    Concatenates a high byte (hb) and a low byte (lb) into a word.
    """
    return np.uint16((hb << 8) | lb)


def get_nibble(value: np.uint16, n: int) -> np.uint16:
    """
    Returns the nth nibble of a number.
    example: get_nibble(0xABCD, 0) = 0xD
    """
    return np.uint16((value & (0xF << (4 * n))) >> (4 * n))


def is_hex(string: str) -> bool:
    """
    Checks if a string is hexadecimal, returns true if so and false otherwise.
    """
    try:
        int(string, 16)
        return True
    except ValueError:
        return False


def split(value: np.uint64) -> list:
    """
    Splits a numerical value into it's composite bytes and returns them in a
    big endian manner.
    """
    rv = [np.uint8(0) for _ in range(8)]
    for i in range(8):
        rv[i] = np.uint8(value & np.uint8(0xFF))
        value >>= np.uint16(8)
    return list(reversed(rv))


def build_uint64(byte_list: list) -> np.uint64:
    """
    Builds a uint64 from a list of bytes.
    """
    rv = np.uint64(0)
    for i in range(8):
        rv = (rv << np.uint64(8)) | np.uint64(byte_list[i])
    return rv


# ANSI character escape sequence for making the terminal output emulator output
# in green.
GREEN = "\033[92m"
# ANSI escape sequence to tell console to stop printing in colour.
ENDC = "\033[0m"


def console_input(prompt_text: str) -> str:  # pragma: no cover
    """
    A wrapper function for python's input function to facilitate unit testing.
    """
    return input(GREEN + prompt_text + ENDC)


def console_output(text: str) -> None:  # pragma: no cover
    """
    A wrapper function for console printing to facilitate unit testing.
    """
    print(GREEN + text + ENDC)


def program_exit():  # pragma: no cover
    """
    A wrapper function for sys.exit.
    """
    sys.exit(0)

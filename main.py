import chip8_util as c8u
import chip8
import sys

def read_bytecode(filename : str) -> list:
    """
    Reads the bytecode from the given file and returns a list of bytes which
    can be loaded into the emulator CPU's memory and run.
    """
    with open(filename, 'r') as code_file:
        code = code_file.read().split()
        # strip out words that would be used as comments, can comment opcodes
        # if preceded by an escape character.
        bytecode = c8u.strip_non_numeric_words(code)
        byte_array = []
        for word in bytecode: # x86 technical reference if anyone cares.
            byte_array.extend(c8u.split(word))
        return byte_array


def main(argc, argv):
    if argc < 2:
        print("Error, need 2 arguments")
    
    if argv[1] == '-t':
        tester = Chip8_Tester()
        tester.run_all_tests()
    else:
        code = read_bytecode(argv[1])
        emu = chip8.Chip8(code)
        emu.execute()

main(len(sys.argv), sys.argv)
import argparse
import struct
import yaml

MEMORY_SIZE = 1024

def execute(binary_file, result_file, memory_range):
    memory = [0] * MEMORY_SIZE
    accumulator = 0

    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    pc = 0
    while pc < len(binary_data):
        opcode = binary_data[pc] & 0xF
        if opcode == 0xD:  # LOAD_CONST
            operand = struct.unpack_from('<I', binary_data, pc)[0] >> 4
            accumulator = operand
            pc += 4
        elif opcode == 0x5:  # LOAD_MEM
            accumulator = memory[accumulator]
            pc += 1
        elif opcode == 0xC:  # STORE_MEM
            address = struct.unpack_from('<I', binary_data, pc)[0]>>4
            memory[address] = accumulator
            pc += 5
        elif opcode == 0x1:  # SHR
            print(list(binary_data))
            address = struct.unpack_from('<I', binary_data, pc)[0]>>4
            print(accumulator,memory[address],accumulator>>memory[address])
            accumulator >>= memory[address]
            pc += 5
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    start, end = map(int, memory_range.split(":"))
    result = memory[start:end]

    with open(result_file, 'w') as f:
        yaml.dump(result, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for UVM")
    parser.add_argument("binary", help="Input binary file")
    parser.add_argument("result", help="Output YAML result file")
    parser.add_argument("memory_range", help="Memory range to save (start:end)")
    args = parser.parse_args()

    execute(args.binary, args.result, args.memory_range)

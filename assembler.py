import argparse
import struct
import yaml

COMMANDS = {
    "LOAD_CONST": 0xD,  # A=13
    "LOAD_MEM": 0x5,    # A=5
    "STORE_MEM": 0xC,   # A=12
    "SHR": 0x1          # A=1
}

def assemble(input_file, output_file, log_file):
    binary_output = bytearray()
    log_output = []

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            cmd = parts[0]
            args = list(map(int, parts[1:]))

            if cmd == "LOAD_CONST":
                opcode = COMMANDS[cmd]
                operand = args[0]
                instruction = struct.pack('<I', (opcode & 0xF) | (operand << 4))
                binary_output.extend(instruction)
                log_output.append({"command": cmd,
                                   "address": operand,
                                   "bytes": [f'0x{b:02X}' for b in instruction]
                                   })

            elif cmd == "LOAD_MEM":
                opcode = COMMANDS[cmd]
                instruction = struct.pack('<B', opcode & 0xF)
                binary_output.extend(instruction)
                log_output.append({"command": cmd, "bytes": [f'0x{b:02X}' for b in instruction]})

            elif cmd == "STORE_MEM":
                opcode = COMMANDS[cmd]
                address = args[0]
                instruction = struct.pack('>BI', (opcode | (address << 4)) & 0xFF,  ((((address >> 4)) & 0xFF) << 24) & 0xFFFFFFFFFF)
                binary_output.extend(instruction)
                log_output.append({"command": cmd, "address": address, "bytes": [f'0x{b:02X}' for b in instruction]})

            elif cmd == "SHR":
                opcode = COMMANDS[cmd]
                address = args[0]
                instruction = struct.pack('>BI', (opcode | (address << 4)) & 0xFF,  ((((address >> 4)) & 0xFF) << 24) & 0xFFFFFFFFFF)
                binary_output.extend(instruction)
                log_output.append({"command": cmd,
                                   "address": address,
                                   "bytes": [f'0x{b:02X}' for b in instruction]
                                   })

    with open(output_file, 'wb') as f:
        f.write(binary_output)

    with open(log_file, 'w') as f:
        yaml.dump(log_output, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for UVM")
    parser.add_argument("input", help="Input file with assembly code")
    parser.add_argument("output", help="Output binary file")
    parser.add_argument("log", help="Log file in YAML format")
    args = parser.parse_args()

    assemble(args.input, args.output, args.log)

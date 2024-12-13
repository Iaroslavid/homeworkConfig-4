import sys
import json
import struct

# Определение команд
COMMANDS = {
    "LOAD_CONST": 0xBF,
    "READ_MEM": 0x4B,
    "WRITE_MEM": 0x53,
    "BITWISE_OR": 0xD9
}

def assemble_line(line):
    tokens = line.split()
    command = tokens[0]

    if command == "LOAD_CONST":
        A = COMMANDS["LOAD_CONST"]
        B = int(tokens[1])
        C = int(tokens[2])

        if not (0 <= C < 64):
            raise ValueError(f"Invalid register address: {C} (must be between 0 and 63)")

        # Формируем команду в формате 5 байтов
        return [A, (B & 0xFF), ((B >> 8) & 0xFF), (C << 2), 0]

    elif command == "READ_MEM":
        A = COMMANDS["READ_MEM"]
        B = int(tokens[1])
        C = int(tokens[2])

        if not (0 <= B < 64 and 0 <= C < 64):
            raise ValueError(f"Invalid register address: B={B}, C={C} (must be between 0 and 63)")

        # Формируем команду в формате 3 байта
        return [A, (B << 2), (C << 2)]

    elif command == "WRITE_MEM":
        A = COMMANDS["WRITE_MEM"]
        B = int(tokens[1])
        C = int(tokens[2])

        if not (0 <= B < 4096 and 0 <= C < 64):
            raise ValueError(f"Invalid address or register: B={B}, C={C}")

        # Формируем команду в формате 4 байта
        return [A, (B & 0xFF), ((B >> 8) & 0xFF), (C << 2)]

    elif command == "BITWISE_OR":
        A = COMMANDS["BITWISE_OR"]
        B = int(tokens[1])
        C = int(tokens[2])

        if not (0 <= B < 64 and 0 <= C < 64):
            raise ValueError(f"Invalid register address: B={B}, C={C} (must be between 0 and 63)")

        # Формируем команду в формате 3 байта
        return [A, (B << 2), (C << 2)]

    else:
        raise ValueError(f"Unknown command: {command}")

def assemble(file_path):
    bin_code = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    cmd_bytes = assemble_line(line)
                    bin_code.extend(cmd_bytes)
                except ValueError as e:
                    print(f"Error in line '{line}': {e}")
                    continue

    return bin_code

def check_byte_range(bin_code):
    for byte in bin_code:
        if not (0 <= byte <= 255):
            raise ValueError(f"Byte {byte} is out of range! Must be between 0 and 255.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("[ Usage: python assembler.py <input_file> <output_bin_file> <output_log_file> ]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_bin_file = sys.argv[2]
    log_file = sys.argv[3]

    # Сборка кода
    bin_code = assemble(input_file)

    # Проверка диапазона байтов
    check_byte_range(bin_code)

    # Запись в бинарный файл
    with open(output_bin_file, 'wb') as binf:
        binf.write(bytes(bin_code))

    # Запись лога в шестнадцатеричном формате
    log_hex = [hex(byte) for byte in bin_code]
    with open(log_file, 'w') as logf:
        json.dump(log_hex, logf, indent=4)

    print(f"Assembly complete. Output written to '{output_bin_file}' and log to '{log_file}'.")

import sys
import json

class VirtualMachine:
    def __init__(self, memSize):
        self.memory = [0] * memSize  # Память
        self.registers = [0] * 2048    # Регистры (64 регистра)
        self.pc = 0                  # Указатель на команду

    def execute(self, binFile):
        with open(binFile, 'rb') as f:
            code = f.read()

        print("Initial Registers:", self.registers)
        print("Initial Memory:", self.memory)
        print("Binary Code:", [hex(b) for b in code])

        while self.pc < len(code):
            instruction = code[self.pc]
            print(f"\nPC: {self.pc}, Instruction: {hex(instruction)}")

            self.pc += 1  # Увеличиваем PC, чтобы перейти к следующему байту
            
            if instruction == 0xBF:  # LOAD_CONST
                B = code[self.pc]
                C = int.from_bytes(code[self.pc + 1:self.pc + 3], 'little')
                self.pc += 3
                self.registers[B] = C
                print(f"LOAD_CONST: R[{B}] = {C}, Registers: {self.registers}")

            elif instruction == 0x4B:  # READ_MEM
                B = code[self.pc]
                C = code[self.pc + 1]
                self.pc += 2
                if self.registers[C] < len(self.memory):  # Проверка на корректный индекс
                    self.registers[B] = self.memory[self.registers[C]]
                    print(f"READ_MEM: R[{B}] = M[R[{C}]] ({self.memory[self.registers[C]]}), Registers: {self.registers}")
                else:
                    print(f"READ_MEM: Invalid memory access at M[R[{C}]] ({self.registers[C]}).")

            elif instruction == 0x53:  # WRITE_MEM
                B = code[self.pc]
                C = code[self.pc + 1]
                self.pc += 2
                if self.registers[B] < len(self.memory):  # Проверка на корректный индекс
                    self.memory[self.registers[B]] = self.registers[C]
                    print(f"WRITE_MEM: M[R[{B}]] = R[{C}] ({self.registers[C]}), Memory: {self.memory}")
                else:
                    print(f"WRITE_MEM: Invalid memory access at M[R[{B}]] ({self.registers[B]}).")

            elif instruction == 0xD9:  # BITWISE_OR
                B = code[self.pc]
                C = code[self.pc + 1]
                self.pc += 2
                if B < len(self.registers) and C < len(self.registers):  # Проверка на валидные индексы
                    self.registers[B] = self.registers[B] | self.registers[C]
                    print(f"BITWISE_OR: R[{B}] = R[{B}] | R[{C}] ({self.registers[B]}), Registers: {self.registers}")
                else:
                    print(f"BITWISE_OR: Invalid register access (B: {B}, C: {C}).")

            else:
                print(f"Unknown instruction {hex(instruction)} at PC: {self.pc - 1}.")
                break  # Завершаем выполнение, если инструкция не распознана

        print("\nFinal Registers:", self.registers)
        print("Final Memory:", self.memory)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[ Usage: python interpreter.py <binary_file> <result_file> ]")
        sys.exit(1)

    binFile = sys.argv[1]
    resFile = sys.argv[2]

    vm = VirtualMachine(memSize=2048)

    # Выполнение команд из бинарного файла
    vm.execute(binFile)

    # Запись результата в файл
    resData = {
        "registers": vm.registers,
        "memory": vm.memory
    }

    with open(resFile, 'w') as f:
        json.dump(resData, f, indent=4)

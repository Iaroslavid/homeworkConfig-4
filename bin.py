with open('output.bin', 'rb') as file:
    # Чтение всех данных в файл
    data = file.read()

# Печать каждого байта в формате 0xXX
print(', '.join(f'0x{byte:02X}' for byte in data))



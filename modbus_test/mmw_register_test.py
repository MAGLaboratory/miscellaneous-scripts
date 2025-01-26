#!/usr/bin/python3 

import minimalmodbus
import time

my_16bit_registers = 0x00
my_16bit_data = [0x1234, 0x5678, 0xABCD, 0xEF12]

my_32bit_data = {0x04: 0xAF12345A, 0x06: 0x005678FF}

my_64bit_data = {0x08: 0xA5123456789AA500}

instr = minimalmodbus.Instrument("COM4", 255)
instr.address = 255
instr.serial.baudrate = 38400
instr.serial.timeout = 0.07

print("Checking communication.")

# check communication
try:
    print(instr.read_registers(0x00, 1))
except:
    print("Communication failed.")
    exit();

time.sleep(1);

print("Writing 16-bit registers")
instr.write_registers(my_16bit_registers, my_16bit_data)

time.sleep(1);

print("Writing 32-bit registers")
for addr, data in my_32bit_data.items():
    instr.write_long(addr, data)

time.sleep(1);

print("Writing 64-bit registers")
instr.write_long(0x08, my_64bit_data[0x08], number_of_registers=4)

time.sleep(1);

print("Now checking registers...")

time.sleep(1);
print("Reading 16-bit registers")
tmp_16bit_data = instr.read_registers(0x00, 4)
assert (tmp_16bit_data == my_16bit_data)
print(tmp_16bit_data)

time.sleep(1);
print("Reading 32-bit registers")
tmp_32bit_data = {}
for addr in my_32bit_data.keys():
    tmp_32bit_data.update({addr: instr.read_long(addr)})
assert (tmp_32bit_data == my_32bit_data)
print (tmp_32bit_data)

time.sleep(1);
print("Reading 64-bit registers")
tmp_64bit_data = {}
for addr in my_64bit_data.keys():
    tmp_64bit_data.update({addr: instr.read_long(addr, number_of_registers=4)})
assert (tmp_64bit_data == my_64bit_data)
print(tmp_64bit_data)

time.sleep(1);
print("Reading 32-bit input registers")
for addr in range(2):
    print(instr.read_long(addr*2, functioncode=4))

time.sleep(1);
print("Reading 16-bit input registers")
for addr in range(4, 8):
    rv = instr.read_registers(addr, 1, functioncode=4)[0]
    if addr < 6:
        print(hex(rv))
    else:
        print(rv)
print("Success!")

#!/usr/bin/python3 

import minimalmodbus
import time

instr = minimalmodbus.Instrument("/dev/ttyUSB0", 255)
instr.address = 255
instr.serial.baudrate = 38400
instr.serial.timeout = 0.5

print("Checking communication.")

# check communication
try:
    print(instr.read_registers(0x00, 2))
except:
    print("Communication failed.")
    exit();

time.sleep(1);

# enter cache mode
instr.write_register(0x01, 0xDEFA)

time.sleep(1);

# configure the board for address 1
instr.write_register(0x02, 257)

time.sleep(1);

# commit the configuration
instr.write_register(0x01, 0x5FAF)

time.sleep(1);

# change the address
instr.address = 1

# check communication
instr.read_registers(0x00, 2)

time.sleep(1);

# write to Flash
instr.write_register(0x01, 0xDEFA)

time.sleep(10);

# check communication one last time
instr.read_registers(0x00, 2)

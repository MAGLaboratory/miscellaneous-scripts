#!/usr/bin/python3 

import minimalmodbus
import time

def print_hex_list(input_list):
    internal_list = ''.join("0x"+format(x, '02x')+"," for x in input_list)
    print(internal_list)

original_address = 1
new_address = 1
new_baudenum = 1
original_baud = 38400
new_baud = 38400


instr = minimalmodbus.Instrument("/dev/ttyUSB0", 255)
instr.address = original_address
instr.serial.baudrate = original_baud
instr.serial.timeout = 0.5


try:
    # check communication
    print("Checking communication.")
    print_hex_list(instr.read_registers(0x00, 2))

    time.sleep(1);

    # enter cache mode
    print("Entering coche mode.")
    instr.write_register(0x01, 0xDEFA)

    time.sleep(1);

    # configure the board for baud mode 1, address 1 
    print("Setting BAUD and Address.")
    brar = (1 << 8 | 1)
    instr.write_register(0x02, brar)

    time.sleep(1);
    # check the brar
    print("Checking configuration.")
    if brar != instr.read_register(0x02):
        raise Exception("Did not write baud rate.")

    time.sleep(1);

    # commit the configuration
    print("Committing the new configuration.")
    instr.write_register(0x01, 0x5FAF)

    time.sleep(1);

    # change the address
    print("Reconfiguring python.")
    instr.address = new_address
    instr.serial.baudrate = new_baud

    # check communication
    print("Checking communication.")
    print_hex_list(instr.read_registers(0x00, 2))

    time.sleep(1);

    # write to Flash
    print("Committing the new configuration to flash.")
    instr.write_register(0x01, 0xDEFA)

    time.sleep(5);

    # check communication one last time
    print("Last communication check.")
    print_hex_list(instr.read_registers(0x00, 2))
except Exception as e:
    print("Failed:")
    print(e)
    exit();

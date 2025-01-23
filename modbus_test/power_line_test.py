#!/usr/bin/python3

import minimalmodbus
import datetime, time, signal

p_exit = 0

def signal_handler(sig, frame):
    global p_exit
    p_exit = 1

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# settings
testing_count = 10000000
progress = False
pnt_time = True
sleep_wait = 0.0

timeout_list = []

for i in range(3):
    timeout_list.append(i * 0.005 + 0.395)


for target_timeout in timeout_list:
    succ = 0
    fail = 0
    c_co = 0
    cons = 0
    errors = ""
    e_counter = 0
    
    instr = minimalmodbus.Instrument("COM4", 255)
    instr.serial.baudrate = 38400
    instr.serial.timeout = target_timeout
    print("Timeout: " + str(instr.serial.timeout))
    if sleep_wait > 0:
        print("Sleep Wait: " + str(sleep_wait))
    # while (not p_exit):
    if pnt_time:
        start_time = datetime.datetime.now()
    for i in range(testing_count):
        try:
            dummy = instr.read_register(0x00, functioncode=4)
            c_co = 0
            succ += 1
            if progress:
                print(".", end = '', flush=True)
        except IOError as err:
            if progress:
                print("x", end = '', flush=True)
            if e_counter < 10:
                errors += str(err)
                errors += "\n"
                e_counter += 1
            c_co += 1
            if c_co > cons:
                cons = c_co
            fail += 1
        if progress and (i % 80 == 79):
            print("")
        if sleep_wait > 0.0:
            time.sleep(0.1)
        if p_exit:
            break
    
    print()
    if pnt_time:
        print("Execution time: {}".format(datetime.datetime.now() - start_time))
    print("Success: " + str(succ), ", Failure: " + str(fail), end='')
    print(", Consecutive Failures: " + str(cons))
    print("Exceptions encountered:")
    print(errors)
    if p_exit:
        break
    

import minimalmodbus
import time, signal

p_exit = 0

def signal_handler(sig, frame):
    global p_exit
    p_exit = 1

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


for target_timeout in [0.22, 0.23, 0.24, 0.25]:
    succ = 0
    fail = 0
    c_co = 0
    cons = 0
    errors = ""
    e_counter = 0
    
    instr = minimalmodbus.Instrument("/dev/ttyUSB0", 1)
    instr.serial.baudrate = 38400
    instr.serial.timeout = target_timeout
    print("Timeout: " + str(instr.serial.timeout))
    
    # i = 0
    
    # while (not p_exit):
    for i in range(1000000):
        try:
            dummy = instr.read_register(0x00, functioncode=4)
            c_co = 0
            succ += 1
            # print(".", end = '', flush=True)
        except IOError as err:
            # print("x", end = '', flush=Truae)
            if e_counter < 10:
                errors += str(err)
                errors += "\n"
                e_counter += 1
            c_co += 1
            if c_co > cons:
                cons = c_co
            fail += 1
        #if (i % 80 == 79):
        #    print("")
        #time.sleep(0.1)
        #i += 1
        if p_exit:
            break
    
    print()
    print("Success: " + str(succ), ", Failure: " + str(fail), end='')
    print(", Consecutive Failures: " + str(cons))
    print("Exceptions encountered:")
    print(errors)
    

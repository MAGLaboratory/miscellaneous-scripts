#!/usr/bin/env python3

import minimalmodbus
import datetime, time, signal
from progress.bar import IncrementalBar

p_exit = 0

def signal_handler(sig, frame):
    global p_exit
    p_exit = 1

# settings
testing_count = 1000
progress = 2
pnt_time = True
pnt_except = True
error_sleep_wait = 0.0
sleep_wait = 0.0
print_report = 1

timeout_list = []
#timeout_list = [0.10, 0.11, 0.12]

queued_info = []

def td_print(info):
    """ Test Data Print """
    queued_info.append(info)
    print(info)
    

def main():
    for target_timeout in timeout_list:
        succ = 0
        fail = 0
        c_co = 0
        cons = 0
        errors = ""
        e_counter = 0
        p_i = -1
        i = 0
        bar_n = 0
        last_bar = time.monotonic()
        
        instr = minimalmodbus.Instrument("COM4", 255)
        instr.serial.baudrate = 38400
        instr.serial.timeout = target_timeout
        instr.clear_buffers_before_each_transaction = False
        td_print(f"Timeout: {str(instr.serial.timeout)}")
        if sleep_wait > 0.0:
            td_print(f"Sleep Wait: {str(sleep_wait)}")
        if progress == 1 or progress >= 4:
            bar = IncrementalBar('Testing', max = testing_count, suffix='%(percent)d%% [%(elapsed_td)s / %(eta)d / %(eta_td)s]')
    
        if progress >= 4:
            print("")
    
        # while (not p_exit):
        if pnt_time:
            start_time = datetime.datetime.now()
        while i < testing_count:
            try:
                dummy = instr.read_registers(0x00, 1)
                c_co = 0
                succ += 1
                if progress == 2 or progress == 5:
                    p_i += 1
                    print("." if progress == 2 else f"\033[F\033[{p_i%80+1}G.\n", end = '', flush=True)
                if progress == 1 or progress >= 4:
                    my_time = time.monotonic()
                    bar_n += 1
                    if (my_time - last_bar >= 0.4):
                        bar.next(bar_n)
                        bar_n = 0
                        last_bar = my_time
            except IOError as err:
                if progress >= 2:
                    p_i += 1
                    print("x" if progress == 2 else f"\033[F\033[{p_i%80+1}Gx\n", end = '', flush = True)
                if progress == 1 or progress >= 2:
                    my_time = time.monotonic()
                    bar_n += 1
                    if (my_time - last_bar >= 0.4):
                        bar.next(bar_n)
                        bar_n = 0
                        last_bar = my_time
                if e_counter < 10:
                    errors += str(err)
                    errors += "\n"
                    e_counter += 1
                instr.serial.flush()
                instr.serial.reset_input_buffer()
                if error_sleep_wait >= 0.0:
                    time.sleep(error_sleep_wait)
                c_co += 1
                if c_co > cons:
                    cons = c_co
                fail += 1
            if (progress >= 2) and (p_i > 0) and (p_i % 80 == 79):
                print("\n" if progress < 4 else "\033[1G\033[X\n", end = '', flush=True)
            if sleep_wait > 0.0:
                time.sleep(sleep_wait)
            i += 1
            if p_exit:
                break
        
        print()
        if pnt_time:
            td_print(f"Execution time: {time.monotonic() - start_time}")
        if progress == 1 or progress >= 4:
            bar.finish()
        td_print(f"Success: {str(succ)}, Failure: {str(fail)}, Consecutive Failures: {str(cons)}")
        if pnt_except:
            print("Exceptions encountered:")
            print(errors)
        if p_exit:
            break

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    
    for i in range(10):
        timeout_list.append(i * 0.001 + 0.006)

    main()

    if print_report:
        print("\033[1mFinal Report\033[0m")
        for info in queued_info: print(info)

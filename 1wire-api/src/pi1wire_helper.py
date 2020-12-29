import glob
import logging
import time
import threading
# from pi1wire import Pi1Wire

import sensor 

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pi1wire_helper')


lock = threading.Lock()

def read_rom(device_file):
    name_file=device_file+'/name'
    with open(name_file,'r') as f:
        return f.readline().strip()
    return ""

def read_temp_raw(device_file):
    with open(f"{device_file}/w1_slave", 'r') as f:
        lines = f.readlines()
        return lines
    return []

def read_temp(device_file):
    startTime = time.time()
    lines = read_temp_raw(device_file)
    elapsedTime = time.time() - startTime
    a = len(lines)
    if a == 0:
        return None, f"{device_file}/w1_slave empy"
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    # return None, "CRC dont match"
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        logger.info(f"read_temp: {device_file} {temp_c} ts: {elapsedTime:0.2}")
        return temp_c, None
    return None, "unknown error"

def readAll():
    with lock:
        out = []
        base_dir = '/sys/bus/w1/devices/'
        # Get all the filenames begin with 28 in the path base_dir.
        device_folder = glob.glob(base_dir + '28*')
        for f in device_folder:
            rom = read_rom(f)
            temp_c, err = read_temp(f)
            # print(f' {f} rom: {rom}')
            if err is None:
                t = sensor.TempSensor(rom, temp_c)
                logger.debug(f"read: file: {rom} {t}")
                out.append(t)
            else:
                logger.error(f"error: {f} {err}")

            # time.sleep(1)
        count = len(out)
        logger.info(f"readAll: {count}")
        return out

# def readSensor(mac: str):
#     s = Pi1Wire().find(mac)
#     print(f)

if __name__ == "__main__":
    FORMAT = '%(asctime)s %(threadName)s/%(thread)d - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    def callReadAll(t):
        logger.info(f"callReadAll({t})")
        ss = readAll()
        for s in ss:
            print(s)


    t1 = threading.Thread(target=callReadAll, args=(1,))
    t2 = threading.Thread(target=callReadAll, args=(2,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # sleep(1000)
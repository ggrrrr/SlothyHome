import logging
from pi1wire import Pi1Wire

import sensor 

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pi1wire')

def readAll():
    out = []
    for s in Pi1Wire().find_all_sensors():
        logger.debug("read: %s" % s)
        t = sensor.TempSensor(s.mac_address, s.get_temperature())
        logger.info("read: %s" % t)
        out.append(t)
    return out

def readSensor(mac: str):
    s = Pi1Wire().find(mac)
    print(f)

if __name__ == "__main__":
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    # logging.basicConfig(format=FORMAT)

    s = readAll()
    print([str(x) for x in s])

import time, logging
from influxdb import InfluxDBClient

import sensor

logger = logging.getLogger('influxdb_helper')

client = None


def config(host: str, port: int = 8086, database: str = "sensors"):
    global client

    client = InfluxDBClient(host=host, port=port)
    # db = client.get_list_database()
    # print(db)
    client.switch_database(database)
    logger.info(f"connected:{host}:{port}:{database}")

def saveSensors(measurement: str, data):
    ts = time.ctime()
    global client
    if client is None:
        raise Exception("not connected")
    mm = []
    for s in data:
        a = TimeSeries(measurement, ts, sensor = s)
        mm.append(a.getData())

    client.write_points(mm)



class TimeSeries:
    def __init__(self, measurement: str, ts, sensor):
        self._measurement = measurement
        self._tags = {}
        self._time = ts
        self._fields = {}
        # if ts is not None:
        self._time = time.ctime()
        self.addSensor(sensor)

    def addSensor(self, s: sensor.RowSensor):
        self._tags["id"] = s.id
        if s.name is not None:
            self._tags["name"] = s.name
        self._fields = s.values

    def getData(self):
        out = {}
        out['measurement'] = self._measurement
        if self._tags is not None:
            out['tags'] = self._tags
        out['time'] = self._time
        out['fields'] = self._fields
        return out

    def __str__(self):
        return  str(self.getData())

if __name__ == "__main__":
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    config(host = "localhost")
    t1 = sensor.TempSensor("3333", 10.3)

    a = TimeSeries("home", time.ctime(), sensor = t1)
    # a.addField({"sasd": 123.12})
    # print(a)
    # saveSensors("home", time.ctime(), [t1])
    client.write_points([a.getData()])

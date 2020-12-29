import sensor
import yaml_helper
import mqtt_helper
import logging
import hashlib 
import pi1wire_helper

logger = logging.getLogger('hass_helper')

def md5(val):
    out = hashlib.md5(val.encode())
    return out.hexdigest()

class HassHelper:

    def __init__(self, topicProfix: str = "homeassistant", decimalPlaces: int = 2):
        self._topicPrefix = topicProfix.strip().strip("/")
        self.decimalPlaces = decimalPlaces

    def _stateTopic(self, sensor: sensor.RowSensor):
        """
        homeassistant/sensor/sensorBedroom/state
        """
        nameHash = md5(sensor.name)
        return f"{self._topicPrefix}/sensor/{nameHash}/state"

    def _configTopic(self, sensor: sensor.RowSensor):
        """
        homeassistant/sensor/sensorBedroomT/config
        """
        nameHash = md5(sensor.name)
        return f"{self._topicPrefix}/sensor/temp/{nameHash}/config"


    def pushTempConfig(self, sensor: sensor.RowSensor):
        if mqtt_helper.client is None:
            return
        if sensor.name is None:
            return
        configTopic = self._configTopic(sensor)
        stateTopic = self._stateTopic(sensor)
        unit = "°C"
        logger.info(f"pushCondig: configTopic:{configTopic}, sensor:{sensor}")
        config = {
            "device_class": "temperature",
            "name": sensor.name,
            "state_topic": stateTopic,
            "unit_of_measurement": unit,
            "value_template": "{{ value_json.temp}}"
        }
        mqtt_helper.client.publish(configTopic, config)

    def pushState(self, sensor: sensor.RowSensor):
        if mqtt_helper.client is None:
            return
        if sensor.name is None:
            return
        stateTopic = self._stateTopic(sensor)
        logger.info(f"pushTemp: configTopic:{stateTopic}, sensor:{sensor}")
        data = {
        }
        if sensor.value("temp") is not None:
            data['temp'] = round(sensor.value("temp"), self.decimalPlaces)
        
        mqtt_helper.client.publish(stateTopic, data)


if __name__ == "__main__":
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    mqtt_helper.config("localhost")

    t1 = sensor.TempSensor("3333", 10.3)
    t1.name = "temp1"


    # a = HassHelper(topicProfix = "asdasdasd")
    a = HassHelper(topicProfix = "hass_auto")
    a.pushTempConfig(t1)
    a.pushState(t1)
    a.pushState(t1)
    a.pushState(t1)
    

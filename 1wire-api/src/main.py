import os
import time
import logging

import sensor
import mqtt_helper
import hass_helper
import yaml_helper
import pi1wire_helper
import cron_helper
import influxdb_helper

logger = logging.getLogger('main')

hass = None

def hendlerMqttHass(msg):
    logger.info("hendlerMqttHass:topic:%s, message:%s" 
        % (msg.topic, msg.payload))
    if msg.payload == b'online':
        sensors = pi1wire_helper.readAll()
        for s in sensors:
            yml = yaml_helper.yamlHelper.read(f"{s.id}.yaml")
            yaml_helper.applyYaml(s, yml)
            hass.pushTempConfig(s)
        for s in sensors:
            hass.pushState(s)

def cronPushState():
    logger.info("cronPushState:")
    sensors = pi1wire_helper.readAll()
    for s in sensors:
        yml = yaml_helper.yamlHelper.read(f"{s.id}.yaml")
        yaml_helper.applyYaml(s, yml)
        hass.pushState(s)
    influxdb_helper.saveSensors("home", sensors)


if __name__ == "__main__":
    FORMAT = '%(asctime)s %(threadName)s/%(thread)d - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    yamlDir = os.getenv("YAML_DIR", "./")
    mqttHost = os.getenv("MQTT_HOST", "localhost")

    hassDecimal = os.getenv("HASS_DECIMAL", 1)
    hassPushTopic = os.getenv("HASS_PUSH_TOPIC", "hass_auto")
    hassStatusTopic = os.getenv("HASS_STATUS_TOPIC", "homeassistant/status")
    cronTask = os.getenv("CRON_TASK", 60)

    influxdbHost = os.getenv("INFLUXDB_HOST", "localhost")

    yaml_helper.config(dir=yamlDir)

    mqtt_helper.config(mqttHost, pubPrefix = "some")

    influxdb_helper.config(host=influxdbHost)

    hass = hass_helper.HassHelper(topicProfix = hassPushTopic, decimalPlaces = hassDecimal)

    mqtt_helper.client.subscribe(hassStatusTopic, hendlerMqttHass)

    mqtt_helper.client.start()

    cron = cron_helper.Periodic(cronTask, cronPushState)

    try:
        while True:
            time.sleep( 10 )
    except KeyboardInterrupt:
        logger.info("exit")
        pass
    cron.stop()
    mqtt_helper.client.stop()

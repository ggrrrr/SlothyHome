import logging
import mqtt_helper
import hass_helper
import yaml_helper
import pi1wire_helper

logger = logging.getLogger('main')

if __name__ == "__main__":
    import time
    import sensor 

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    yaml_helper.config(dir="/home/pi/slothyHome/SlothyHome/1wire-api")
    mqtt_helper.config("mqtt-host", pubPrefix = "some")
    # mqtt_helper.client.publish("asd", "msg")

    hass = hass_helper.HassHelper(topicProfix = "hass_auto")

    mqtt_helper.client.subscribe("homeassistant/status", hass.hendlerHass)

    mqtt_helper.client.start()

    try:
        while True:
            time.sleep( 10 )
    except KeyboardInterrupt:
        logger.info("exit")
        pass

    mqtt_helper.client.stop()

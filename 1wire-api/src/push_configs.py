import logging
import mqtt_helper
import hass_helper
import yaml_helper
import pi1wire_helper

logger = logging.getLogger('push_configs')

if __name__ == "__main__":
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
        
    mqtt_helper.config("hass-host")
    yaml_helper.config()

    hass = hass_helper.HassHelper(topicProfix = "hass_auto")

    sensors = pi1wire_helper.readAll()
    for s in sensors:
        yml = yaml_helper.yamlHelper.read(f"{s.id}.yaml")
        yaml_helper.applyYaml(s, yml)
        hass.pushTempConfig(s)
        # hass.pushState(s)
        # print(s)
        # pass

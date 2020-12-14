import yaml
import logging
import sensor


logger = logging.getLogger('yaml-helper')

yamlHelper = None

def applyYaml(sensor: sensor.RowSensor , yamlConfig: dict):
    if sensor is None:
        return
    if yamlConfig is None:
        return
    logger.debug(f"applyYaml.sensor[{sensor.id}]:  from: {sensor}")
    if "name" in yamlConfig:
        sensor.name = yamlConfig['name']
    if "values" in yamlConfig:
        values = yamlConfig['values']
        if isinstance(values, list):
            for v in values:
                if "offset" in v:
                    name = v['name']
                    offset = v['offset']
                    sensor.offsetValue(name, offset)
    logger.info(f"applyYaml.sensor[{sensor.id}]:  updated: {sensor}")

class YamlHelper:

    def __init__(self, dir):
        self.dir = "%s/" % dir.rstrip("/")

    def read(self, filename):
        # pass
        f = f"{self.dir}{filename}"
        logger.info(f"open: {f}")
        try:
            with open(f, "r") as file:
                try:
                    return yaml.load(file, Loader=yaml.FullLoader)
                except yaml.YAMLError as e:
                    logger.error("YAML error: %s, %s" % ( type(e) ,e) )
                    return {}
        except FileNotFoundError:
            return {}


def config(dir = "./"):
    global yamlHelper
    yamlHelper = YamlHelper(dir)

if __name__ == "__main__":
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    config("./")

    asd = yamlHelper.read("280119141149f3.yaml")
    print(f"{asd}")
    # if f"{asd}" != "{'name': 'shit', 'type': 'temp'}":
        # raise Error("")

    t1 = sensor.TempSensor("2222", 23.1)
    applyYaml(t1, asd)
    # print(t1)

    # asd = yamlHelper.read("asd.yaml")
    # print(asd)
    # # print(f"{asd}")
    # if f"{asd}" != "{}":
    #     raise Error("")

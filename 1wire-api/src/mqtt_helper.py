import json
import logging
import paho.mqtt.client as mqttClient

logger = logging.getLogger('mqtt_helper')

client = None

def formatMsg(msg):
    logger.debug("formatMsg: type:%s" % type(msg))
    if isinstance(msg, str):
        return bytes(msg, 'utf-8')

    if isinstance(msg, dict):
        a = json.dumps(msg)
        return bytes(a, 'utf-8')

    return msg

class MqttClient:

    def __init__(self, host: str, port: str = 1883, pubPrefix:str = None):
        self.mqttHost = host
        self.mqttPort = port
        self.client = None
        self.pubPrefix = pubPrefix


    def publish(self, topic, msg):
        if msg is None:
            return
        if self.client is None:
            logger.debug("mqtt:client not connected")

        topic1 = self.formatTopic(topic)
        data = formatMsg(msg)
        logger.debug("publish: topic:%s: data:%s" % (topic1, data) )
        self.client.publish("%s" % topic1, data)


    def on_connect(self, client, userdata, flags, rc):
        logger.info("on_connect: %s %s, %s" %(  client, userdata, msg, ))
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        logger.info("on_message:client:%s, userdata:%s, topic:%s, message:%s" %(  client, userdata, msg.topic, msg.payload ))

    def formatTopic(self, topic):
        if self.pubPrefix is None:
            return topic
        return f"{self.pubPrefix}/{topic}"

    def connect(self):
        logger.info(f"connect: {self.mqttHost}:{self.mqttPort}")
        client = mqttClient.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
    
        client.connect(self.mqttHost, self.mqttPort, 60)
        # client.subscribe(args.mqttTopic)
        client.subscribe("cmd")
        client.subscribe("switch/#")
        logger.info("mqttInit." % ())
        self.client = client
        # return client

def config(host: str, port: str = 1883, pubPrefix:str = None):
    global client
    client = MqttClient(host, port = port)
    client.connect()


if __name__ == "__main__":
    import time
    import sensor 

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    config("mqtt-host", pubPrefix = "some")
    client.publish("asd", "msg")
    # sleep(123)

    t1 = sensor.TempSensor("3333", 10.3)
    client.publish("temp", t1.json())

    time.sleep( 1 )
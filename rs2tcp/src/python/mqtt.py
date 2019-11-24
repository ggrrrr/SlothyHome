# MQTT support

import logging
import time
import paho.mqtt.client as mqtt

# def mqttOnMessage(client, userdata, msg):
#         print("_mqttOnMessage: %s %s %s" % (client, userdata, msg))

def initArgument(parser):
    parser.add_argument('--mqttHost', default='localhost'
        , dest='mqttHost', help='Mqtt host default localhost')
    parser.add_argument('--mqttPort', default=1883
        , dest='mqttPort', type=int, help='Mqtt port default 1883')
    parser.add_argument('--mqttTopicCommand', default="cmd"
        , dest='mqttTopicCommand', help='Mqtt topic for commands')
    parser.add_argument('--mqttTopicStatus', default="status"
        , dest='mqttTopicStatus', help='Mqtt Topic Status')
    parser.add_argument('--mqttTopicPrefix', default=""
        , dest='mqttTopicPrefix', help='Mqtt topic prefix')

class SlothyMqtt(object):

    _client = None

    _instance = None

    _mqttHost = None
    _mqttPort = None
    _mqttTopic = None
    _mqttPrefix = None

    _commandSwitchFunction = None

    # def __new__(cls, args):
    #     logging.info("__new__:")

    def setCommandSwitchFunction(self, commandSwitchFunction):
        self._commandSwitchFunction = commandSwitchFunction

    def connect(self):
        logging.info("conect:... ")
        self._client = mqtt.Client()
        self._client.on_connect = self._mqttOnConnect
        self._client.on_message = self._mqttOnMessage

        self._client.connect(self._mqttHost, self._mqttPort, 60)
        self._client.subscribe(self._mqttTopicCommand)
        self._client.loop_start()
        # self._client.loop()
        # self._client.start()
        # self._client.subscribe("light/#")

    def _mqttOnConnect(self, client, userdata, flags, rc):
        logging.debug("_mqttOnConnect: %s %s %s %s %s" % (client, userdata, flags, rc))

    def _mqttOnMessage(self, client, userdata, msg):
        logging.info("_mqttOnMessage: t:%s m:%s" %
            (msg.topic, msg.payload))

    def __init__(self, args):
        logging.info("__init__: %s" % (args))
        if 'mqttHost' in args:
            self._mqttHost = args.mqttHost
        if 'mqttPort' in args:
            self._mqttPort = args.mqttPort
        if 'mqttTopicCommand' in args:
            self._mqttTopicCommand = args.mqttTopicCommand

    def __del__(self):
        logging.info("__del__")

    def callBackSwitchStatus(self, id, status):
        logging.info("callBackSwitchStatus:FIXME:%s ", msg)

    def commandSwitchOn(self, id):
        logging.info("commandSwitchLow:FIXME:%s ", msg)

    def commandSwitchOff(self, id):
        logging.info("commandSwitchHigh:FIXME:%s ", msg)

    def commandSwitch(self, id):
        logging.info("commandSwitch:FIXME:%s ", msg)

    def close(self):
        if self.__client is None:
            return
        self.__client.disconnect()

if __name__ == '__main__':
    print("main")
    logging.basicConfig(level=logging.DEBUG)
    import argparse
    parser = argparse.ArgumentParser(description='slothy MQTT test tool.')
    initArgument(parser)
    args = parser.parse_args()
    a = SlothyMqtt(args)
    a.connect()
    try:
        # serReady = 1
        while 1:
            pass
    except KeyboardInterrupt:
        logging.info("main: KeyboardInterrupt")
        # pass
    a.close()
    # logging.info("stoped: ser: %s" % ser)


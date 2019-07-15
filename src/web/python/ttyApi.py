#!/usr/bin/python3
# Provides:          slothyHome-tty.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.

# https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

import sys
import _thread
import argparse
import logging
import socket
import time
import paho.mqtt.client as mqtt
import signal

from tty import SlothyTty
from rest import SlothyHttp

logging.basicConfig(level=logging.INFO)

def remapStatusFromHa(s):
    if "ON" == s:
        return "h"
    if "on" == s:
        return "h"
    if "On" == s:
        return "h"
    if "1" == s:
        return "h"
    return "l"

def remapStatusToHa(s):
    if int(s) == 1:
        return "on"
    return "off"

def parseTtyCallBack(mqtt, lines):
    logging.debug("parseTty: %s" % lines)
    for line in lines:
        cmd = line[0:3]
        logging.debug("parseTty:cmd:%s" % ( cmd ))
        if "led" == cmd:
            lightId = line[4]
            # bytes("%s\n" % data, 'utf-8')
            status = bytes(remapStatusToHa(line[6]), 'utf-8')
            logging.debug("parseTtyCallBack:light: %s, status: %s" % ( lightId, status ))
            mqtt.publish("light/%s/status" % lightId, status)
        # if line == "led":
        #     mqtt.publish("light/1/status","OFF")
        # if line == "led:0:1":
        #     mqtt.publish("light/1/status","ON")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("on_connect: %s %s, %s" %(  client, userdata, msg, ))
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info("on_message:client:%s, userdata:%s, topic:%s, message:%s" %(  client, userdata, msg.topic, msg.payload ))
    # print(msg.topic+" "+str(msg.payload))
    if "cmd" == msg.topic:
        tty.sendData("%s" % msg.payload.decode("utf-8") )
        return

    ll, lightId, lightCmd = msg.topic.split("/")
    if "switch" == lightCmd:
        ledCmd = remapStatusFromHa(msg.payload.decode("utf-8") )
        tty.sendData("wlc%s" % lightId )
        return

def mqttInit(args):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(args.mqttHost, 1883, 60)
    # client.subscribe(args.mqttTopic)
    client.subscribe("cmd")
    client.subscribe("light/#")
    return client

_LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

def _log_level_string_to_int(log_level_string):
    if not log_level_string in _LOG_LEVEL_STRINGS:
        message = 'invalid choice: {0} (choose from {1})'.format(log_level_string, _LOG_LEVEL_STRINGS)
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)
    # check the logging log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)

    return log_level_int

def signalTerm(signum, frame):
    print('Signal handler called with signal', signum)
    # raise OSError("Couldn't open device!")
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='slothy API.')
    parser.add_argument('--ttyDev', default=None, dest='ttyDev', help='set tty dev file')
    parser.add_argument('--ttyRate', default=9600, dest='ttyRate', type=int, help='set port rate: 9600, 19200, 38400, 57600...')
    
    parser.add_argument('--httpPort', default=None, dest='httpPort', type=int, help='start http on port if set!')
    parser.add_argument('--httpHost', default='0.0.0.0', dest='httpHost', help='http listen port default 0.0.0.0')
    parser.add_argument('--mqttHost', default=None, dest='mqttHost', help='Mqtt host default pi-01')
    parser.add_argument('--mqttPort', default=1883, dest='mqttPort', type=int, help='Mqtt port default 1883')
    parser.add_argument('--mqttTopic', default="test", dest='mqttTopic', help='Mqtt topic sub')
    parser.add_argument('--mqttTopicPrefix', default="", dest='mqttTopicPrefix', help='Mqtt topic prefix')
    parser.add_argument('--logLevel', default="INFO", type=_log_level_string_to_int, dest='logLevel', help='log level')

    args = parser.parse_args()
    logging.info("args: %s" % (args))
    logging.getLogger().setLevel(args.logLevel)

    if args.ttyDev is None:
        devices = SlothyTty.listDevices()
        for port in devices:
            print("device: {}, name: {}, description: {}/{}".format(
                port['device'], port['name'], port['description'], port['sn'])
                )
        sys.exit(1)

    if args.mqttHost is not None:
        mqtt = mqttInit(args)
        mqtt.loop_start()

    tty = SlothyTty(args)

    tty.connect()
    tty.callBack = parseTtyCallBack
    tty.mqtt = mqtt
    tty.readData()
    # thread.start_new_thread( readLoop, () )

    if args.httpPort is not None:
        http = SlothyHttp(tty=tty, args=args)

    _thread.start_new_thread ( tty.readLoop, () )
    signal.signal(signal.SIGTERM, signalTerm)
    try:
        # serReady = 1
        while 1:
            http.server.handle_request()
            pass
    except KeyboardInterrupt:
        logging.info("main: KeyboardInterrupt")
        # pass
    tty.close()
    logging.info("stoped: ser: %s" % ser)

    # if args.httpPort is not None:
        # httpInit(args)

    # mqttInit(args)

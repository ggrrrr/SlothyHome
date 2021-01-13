#!/bin/bash

docker run -d --name sensors --privileged \
    -v /sys:/sys \
    -v /dev:/dev \
    -v /home/pi/sensors:/data \
    --net=host \
    -e YAML_DIR=/data \
    -e MQTT_HOST=localhost \
    slottyhome/sensors:latest \
    python main.py


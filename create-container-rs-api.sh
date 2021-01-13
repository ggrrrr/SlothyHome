#!/bin/bash

docker run -d --name rs-api --privileged \
    -v /dev:/dev \
    -p 8080:8080 \
    --net=host slottyihome/rs-api:latest \
    python src/python/ttyApi.py \
        --ttyDev /dev/ttyACM0 \
	--ttyRate 38400 \
        --httpPort 8080 \
        --mqttHost "mqtt-host" \
        --mqttPort 1883 \
        --mqttTopic test


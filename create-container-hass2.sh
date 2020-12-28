#!/bin/bash

docker run -d --name hass2 --privileged \
	-v /home/pi/hass:/config \
	--net=host \
	homeassistant/home-assistant:stable



#!/bin/bash

docker run -d --name hass --privileged \
	-v /home/pi/homeassistant:/config \
	-p 8123:8123 --net=host \
	homeassistant/home-assistant:stable



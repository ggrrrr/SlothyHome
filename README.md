# Slothy Home

## This project is to enable all lights/fans in a house/apartment to be controlled via Arduino MCU (_single if possible board_) and optional via systems like [HomeAutomation](https://www.home-assistant.io) or [Domoticz](http://domoticz.com)

## All lights/fans are GPIO of the Arduino and the switches are buttons via Shift register (*74HC165*).

## The idea is to have all lights cables terminated closed to Arduino MCU board and connect many SSR or normal relay direclty to the Arduino GPIO pins

## _TODO_
* PWM controled lights - *need to work on PWM schematic and controller*
* I2C temp, and other - *it is quite slow when reading*
* Second RS485 for Serial CLI - *to enable multiple Arduino boards with single computer system*

## Short description of data flow
* (Arduino `buttons.ino` Firmware) <- Serial CLI -> (`ttyApi.py`) <- HTTP REST and/or MQTT -> (HomeAutomation or Domoticz)

## REST Service
* Example service start without MQTT
  * `python3 src/web/python/ttyApi.py  --httpPort 8080 --ttyDev /dev/cu.usbmodem2301`
* TODO Example service start with MQTT
  * `python3 src/web/python/ttyApi.py --mqttHost mqtt.host --mqttPort 1883 --httpPort 8080 --ttyDev /dev/cu.usbmodem2301`
* Example REST call
  * `curl "http://localhost:8080/send?cmd=wlg1"`

## Arduino PIN connections

### Ardiuno LED PINs
* 53 - 30 Ardiuno PIN
* PIN 53 -> Button index 0
* PIN 52 -> Button index 1
* PIN 51 -> Button index 2
* ....

### Ardiuno Shift Register PIN
* PIN  8 to SH/!LD (shift or active low load) - Pin 1 (!PL) of 74HC165
* PIN  9 to !CE (clock enable, active low) - Pin 15 (!CE) of 74HC165
* PIN 11 to SER_OUT (Serial data out) - Pin 9 (Q7) of 74HC165
* PIN 12 to CLK (the clock that times the shifting) - Pin 2 (CP) of 74HC165

## Arduino TTY CLI help
* `re` - Read Eeprom -> Read all internal EEPROM
  * response:
    ```
    cmd:re
    eeprom:0:1
    EEPROM:<BUTTON INDEX>:<BIT MAP of all LED PINs >
    eeprom:1:10 --> button 2 will control first second and thirt LED PINs (LED PIN 52)
    eeprom:2:111 --> button 2 will control first second and thirt LED PINs (LED PIN 53, 52 51)
    ....
    ```
* `rl` - Read Light
* `wl...` - Write Light
  * `wlcNN` - Write Light Change
  * `wlgNN` - Write Light Group 
* `we...` - Write Eeprom
  * example `we00b11111111` - 
    * `we` (Write Eprom)
    * `00` (button index) Decimal number 00 -> 0, 01 -> 1 ...
    * `b`  (binary)
    * `11111111` (bit map) the actual bit map of the LED INDEX ( 0, 1, 2, 3, 4 , 5, 6, 7)
* `I` - Init EEPROM



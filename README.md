# **Slothy Home**

## **SlothyHome** has these main objectives
* Basic functionality to run on simple device - easy to fix easy to replace, fast boot time
  * function like switching on/off lights, fans, heaters etc.
  * accept commands of buttons/switches , temp sensors, door sensors, humidity etc.
* Complex functionality to run on complex device - more and more options, upgrades, updates etc
  * Monitoring
  * Mobile / Remote access
  * Logging
  * Statistics
  * Notifications
  * Scheduling of tasks
  * AI
  * Backup
* To have freedom to select any computer system for the complex part
 
In general the idea is to split the system in to two main sub systems.
### _System 1_ to control all **basic house hold items** lights, fans etc. To be very small and simple, with very very tiny firmware. After some time to have stable firmware version (limited to the MCU), and there will be no need of updates/upgrades/restarts.
### _System 2_ API to the _System 1_ to be computer based software. All upgrades/updates and other changes of that system will not effect the people who are living in the premises, to use as standard as possible protocols.

## **SlothyHome** implementation choice

  ### __SlothyHome MCU Buttons__ Arduino - _System 1_
    * Arduino 
      * cheep 
      * open source
      * many docs
    * Serial CLI easy to implement on MCU and PC
      * RS232 very easy 1to1 connection
      * RS485 many to many serial connection __TODO__

  ### __SlothyHome API__ with MQTT and REST support - _System 2_
    * MQTT is very well suited status update
    * REST is very well suited for setup and control

## **SlothyHome MCU** functionality TBC
* **Switch** - these are actial OUT pins of the MCU, to control lights, fans heaters etc.
  * controlled output PIN
  * group pins
  * switch off delay _TODO_
  * Status udpate via RS
* **PWM** - _TODO_
  * Status udpate via RS
* **Buttons** - these are IN pins, multiplied via "shift register" see 74HC165 or other
  * configure which buttons index controls which Switch Group
  * multiple buttons to control single Switch group
  * status update via RS
* **I2C temp, humidity, sensors ...** _TODO_
  * I2C on arduino in general generates very slow responses and can disrupt other functionality
  * if implemented in the same firmware or additional MCU
* **Heating control**
  * ___TBC___ Same firmaware other etc...
* **Doors/windows sensors**
  * ___TBC___
* **KNX**
  * __TBC___

## **SlothyHome project folders**
* `arduino/buttons/` -> __SlothyHome MCU Buttons__ firmware
* `gui/src/python/` -> __SlothyHome GUI__ Touch screens UI
* `rs2tcp/src/python/` -> __SlothyHome API__ Interface between Serial CLI and any REST/MQTT sub systems 
* `raspbian/boot/` -> Some help for raspbian
* `etc/` -> some help files GUI for linux lxde startup scripts 

## Additional reading
* [Python 3](https://www.python.org/download/releases/3.0/)
* [Python MQTT Paho Lib](https://pypi.org/project/paho-mqtt/)
* [HomeAutomation](https://www.home-assistant.io)
* [Domoticz](http://domoticz.com)
* [KNX](https://my.knx.org)

## All lights/fans are GPIO of the Arduino and the switches are buttons via Shift register (*74HC165*).

## In additonal to avoid using WiFi as much as possble for not mobile items
## Wiring preconditions
* The idea is to have all lights power cables directly terminated next to Arduino MCU board and use SSR or normal relay to the GPIO pins
  * SSR options:
    * [8 Channel 2A 220VAC SSR Board High Level Trigger...](https://www.aliexpress.com/item/32960022800.html?spm=a2g0s.9042311.0.0.c6a34c4dliea0c)
    * [MRA-23D2 Mini 6.2mm 2A 220VAC SSR DIN Rail Switch Relay...](https://www.aliexpress.com/item/32889489536.html?spm=a2g0s.9042311.0.0.27424c4dKvJlVF)
* All switches/buttons cables to be also directly terminated next to the MCU board. Also there will be only 5V DC running on these so very very **safe**, runnning UTF/FTP can be used.

## _TODO_
* Proper JSON REST responses
* ADC for 220V AC amp meter
* PWM controlled lights - *need to work on PWM schematic and controller*
* I2C temperature, and other sensors - *it is quite slow when reading*
* Second RS485 for Serial CLI - *to enable multiple Arduino boards with single computer system*
* Off time delay par PIN - this can be used for fan in WC
* give proper naming of PIN index, lights and buttons/switches - __proper abbreviations and names__
* allow PIN and switches labeling in the EEPROM :-)
* change behavior between _push button_ and _light switch_
* more configs in the EEPROM

## Short description of data flow
* Signal from push button _5V_
  * Shift register _5V_
  * `buttons.ino` (Arduino Firmware)
    * _GPIO PIN SET_
    * _Serial CLI_ **status update** 
      * `ttyApi.py` _SlothyHome service_
      * `HTTP REST | MQTT`
      * _HomeAutomation or Domoticz or other..._

* _HomeAssistant or Domoticz_ command for lights command
  * `HTTP REST | MQTT`
  * `ttyApi.py` _SlothyHome service_
  * _Serial CLI_ **control command** 
  * `buttons.ino` (Arduino Firmware)
    * _GPIO PIN SET_
    * _Serial CLI_ **status update**
      * ... 

# Some HOWTOs

## REST Service
* Example service start without MQTT
  * `python3 src/web/python/ttyApi.py  --httpPort 8080 --ttyDev /dev/cu.usbmodem2301`
* TODO Example service start with MQTT
  * `python3 src/web/python/ttyApi.py --mqttHost mqtt.host --mqttPort 1883 --httpPort 8080 --ttyDev /dev/cu.usbmodem2301`
* Example REST call
  * `curl "http://localhost:8080/send?cmd=wlg1"`


## Shift Register(s) 74HC165 wiring
* __TODO add link schematic__

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
* `rl` - Read Light **status update** *FIXME proper name*
* `wl...` - Write Light **control command** *FIXME proper name*
  * `wlcNN` - Write Light Change
  * `wlgNN` - Write Light Group 
* `we...` - Write Eeprom
  * example `we00b11111111` - 
    * `we` (Write Eprom)
    * `00` (button index) Decimal number 00 -> 0, 01 -> 1 ...
    * `b`  (binary)
    * `11111111` (bit map) the actual bit map of the LED INDEX ( 0, 1, 2, 3, 4 , 5, 6, 7)
* `I` - Init EEPROM

## Other hardware
* DS2406 - 1-Wire GPIO PIO-A (IN)) ( door sensor)
* DS2413 - 1-Wire GPIO PIO-A (OUT) PIO-B (IN) (door sensor and LED)
* DS18B20 - 1-Wire Temp sensor

## Home Assistant examples and tools
* HASS Docs
  * https://www.home-assistant.io/docs/
* icons:
  * https://cdn.materialdesignicons.com/4.7.95/
* exmaple configuration.yaml: 
```YAML
...
mqtt:
  broker: 192.168.4.1

switch: !include switch.yaml
...
```
* exmaple configuration.yaml: 
```YAML
  - platform: mqtt
    name: "switch 0"
    state_topic: "switch/0/status"
    command_topic: "switch/0/set"
    payload_on: "on"
    payload_off: "off"
    state_on: "on"
    state_off: "off"
    optimistic: false
    qos: 0
    retain: true
```



# Ardiuno LED PINs
* 53 - 30 Ardiuno PIN
* PIN 53 -> Button index 0 
* PIN 52 -> Button index 1 
* PIN 51 -> Button index 2
* .... 


# Ardiuno Shift Register PIN
* PIN  8 to SH/!LD (shift or active low load) - Pin 1 (!PL) of 74HC165
* PIN  9 to !CE (clock enable, active low) - Pin 15 (!CE) of 74HC165
* PIN 11 to SER_OUT (Serial data out) - Pin 9 (Q7) of 74HC165
* PIN 12 to CLK (the clock that times the shifting) - Pin 2 (CP) of 74HC165

# Arduino TTY CLI help
* re - Read Eeprom -> Read all internal EEPROM
```
cmd:re
eeprom:0:1
EEPROM:<BUTTON INDEX>:<BIT MAP of all LED PINs >
eeprom:1:10 --> button 2 will control first second and thirt LED PINs (LED PIN 52)
eeprom:2:111 --> button 2 will control first second and thirt LED PINs (LED PIN 53, 52 51)
....
```
* rl - Read Light
* wl - Write Light
* we - Write Eeprom
  * we00b11111111 - 
    * we (Write Eprom)
    * 00 (button index) Decimal number 00 -> 0, 01 -> 1 ...
    * b  (binary)
    * 11111111 (bit map) the actual bit map of the LED INDEX ( 0, 1, 2, 3, 4 , 5, 6, 7)
* I - Init EEPROM



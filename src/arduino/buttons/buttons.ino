#include <EEPROM.h> //Needed to access the eeprom read write functions

// SHIFT REGISTER 74HC165
#define SHIFT_CHIPS 2
#define SHIFT_PULSE_WIDTH_USEC   5
#define SHIFT_POLL_DELAY_MSEC   1

#define SHIFT_PLOAD_P 8  // Connect Pin 8 to SH/!LD (shift or active low load) - Pin 1 (!PL) of 74HC165
#define SHIFT_CE_P    9  // Connect Pin 9 to !CE (clock enable, active low) - Pin 15 (!CE) of 74HC165
#define SHIFT_DATA_P  11 // Connect Pin 11 to SER_OUT (Serial data out) - Pin 9 (Q7) of 74HC165
#define SHIFT_CLOCK_P 12 // Connect Pin 12 to CLK (the clock that times the shifting) - Pin 2 (CP) of 74HC165

uint32_t pinValues;
uint32_t oldPinValues;

// Cinpik
const String COMPILE_DATE = __DATE__ " " __TIME__;  //compile date that is used for a unique identifier

//FIXME make it eeprom
const int     BUTTON_COUNT = SHIFT_CHIPS * 8;
const int     LED_COUNT = 8 * 3;
const uint8_t ledPins[LED_COUNT] = 
    {53,52,51,50,49,48,47,46
    ,45,44,43,42,41,40,39,38
    ,37,36,35,34,33,32,31,30
    };

unsigned long ledGroupMap[LED_COUNT];
int ledGroupState[LED_COUNT];
uint8_t ledStates[LED_COUNT];

int RESET_PIN = 7;

int incomingByte = 0;   // for incoming serial data

const long timerInterval = 21000; // interval at which to blink (milliseconds)
unsigned long previousMillis = 0;        // will store last time LED was updated


int readCmdNumber( String number) {
  return number.toInt();
}

// Serial send done"."
void sendDone() {
  Serial.println(".");
}

void heartBeatResponse() {
  Serial.println("ok");
}

void heartBeatRequest() {
  Serial.println("hb");
}

void sendCompileDate() {
  Serial.print("VER:");
  Serial.println(COMPILE_DATE);
}

void sendInfoLed(int idx) {
  Serial.print("led:");
  Serial.print(idx);
  Serial.print(":");
  Serial.print(ledStates[idx]);
  Serial.println("");
}

void sendInfoEEPROM() {
  for (int i = 0; i < BUTTON_COUNT; i++) {
    Serial.print("eeprom:");
    Serial.print(i);
    Serial.print(":");
    Serial.print(ledGroupMap[i], BIN);
    Serial.println();
//    Serial.print(":");
  }
}

void setLedGroupMap(int bIdx, uint32_t ledIdx) {
  ledGroupMap[bIdx] = ledIdx;
}

void eepromWriteGroupMap(int p_address, int gIdx, uint32_t ledMap) {
  int add = p_address + (4 * gIdx);
  uint8_t ledMap0 = ledMap;
  uint8_t ledMap1 = ledMap >> 8;
  uint8_t ledMap2 = ledMap >> (8 * 2);
  uint8_t ledMap3 = ledMap >> (8 * 3);
  Serial.print("i:eeprom:write:");
  Serial.print(add);
  Serial.print(":");
  Serial.print(gIdx);
  Serial.print(":");
  Serial.print(ledMap, BIN);
  Serial.println();
  EEPROM.write(add, ledMap0);
  EEPROM.write(add + 1, ledMap1);
  EEPROM.write(add + 2, ledMap2);
  EEPROM.write(add + 3, ledMap3);
  setLedGroupMap(gIdx, ledMap);
}

void writeDefaultEEPROM(int p_address) {
  Serial.println("i:eeprom:defaut:");
  for (int i = 0; i < LED_COUNT; i++) {
    uint32_t ledMap =  (uint32_t)1 << i;
    eepromWriteGroupMap(0, i, ledMap);
    p_address ++;
  }
}

void readEEPROM(int p_address) {
  for (int i = 0; i < BUTTON_COUNT; i++) {
    int add = p_address + (4 * i);
    uint32_t ledMap0 = EEPROM.read(add);
    uint32_t ledMap1 = EEPROM.read(add+1);
    uint32_t ledMap2 = EEPROM.read(add+2);
    uint32_t ledMap3 = EEPROM.read(add+3);
    uint32_t ledMap = ledMap0 | (ledMap1 << 8);
    Serial.print("i:eeprom:");
    Serial.print(add);
    Serial.print(":");
    Serial.print(i);
    Serial.print(":");
    Serial.print(ledMap, BIN);
    Serial.println();
    setLedGroupMap(i, ledMap);
  }
}

void heartBeatEvent() {
  heartBeatRequest();
  sendDone();
}

void ledChage(int idx, int state) {
  if ( idx >= 0 && idx < LED_COUNT) {
    digitalWrite(ledPins[idx], state);
    ledStates[idx] = state;
    sendInfoLed(idx);
  } else {
    Serial.print("ERR IDX:");
    Serial.println(idx);
  }
}

void ledUp(int idx) {
  ledChage(idx, HIGH);
}

void ledDown(int idx) {
  ledChage(idx, LOW);
}

void ledChange(int idx) {
  int ledState = ledStates[idx] ? LOW : HIGH;
  ledChage(idx, ledState);
}

void buttonFell(int idx) {
//  int ledIdx = buttonMap[idx];
  ledChange(idx);
  sendDone();
}

int readline(int readch, char *buffer, int len) {
  static int pos = 0;
  int rpos;

  if (readch > 0) {
    switch (readch) {
      case '\r': // Ignore CR
        break;
      case '\n': // Return on new-line
        rpos = pos;
        pos = 0;  // Reset position index ready for next time
        return rpos;
      default:
        if (pos < len - 1) {
          buffer[pos++] = readch;
          buffer[pos] = 0;
        }
    }
  }
  return 0;
}

void readLight(String cmd) {
  byte idxB = cmd[2];
  if ( idxB == 0 ) {
    for (int i = 0; i < LED_COUNT; i++) {
      sendInfoLed(i);
    }
    return;
  }
  int idx = idxB - '0';
  sendInfoLed(idx);
}

void chageLedGroupMap(int mapIndex) {
    uint32_t bm = ledGroupMap[mapIndex];
    int toState = ! ledGroupState[mapIndex];
    ledGroupState[mapIndex] = toState;
    for (int bits = 31; bits > -1; bits--) {
      if (bm & ((uint32_t )1 << bits)) {
        ledChage(bits, toState);
      }
    }
}

void writeLight(String cmd) {
  char lCmd = cmd[2];
  byte idxB = cmd[3];
  if ( idxB == 0 ) {
    return;
  }
  int idx = readCmdNumber(cmd.substring(3));

  switch (lCmd) {
    case 'c':
      ledChange(idx);
      break;
    case 'h':
      ledUp(idx);
      break;
    case 'l':
      ledDown(idx);
      break;
    case 'g':
      chageLedGroupMap(idx);
      break;
    default:
      Serial.println("ERR L CMD");
  }
  //  sendInfoLed(idx);
}

void writeEEPROM(String cmd) {
  String idxStr = cmd.substring(2,4);
  String typeStr = cmd.substring(4,5);
  String valStr = cmd.substring(5);
  int idx = idxStr.toInt();
  uint32_t tt = strtoul(valStr.c_str(), 0, 2);
  eepromWriteGroupMap(0, idx, tt);
}


// Process "r"-read comands
void processRead(String cmd) {
  switch (cmd[1]) {
    case 'l':
      readLight(cmd);
      break;
    case 'e':
      sendInfoEEPROM();
      sendCompileDate();
      break;
    case 'b':
      Serial.println("button:TODO");
      break;
    case 'g':
      Serial.println("group:TODO");
      break;
    default:
      Serial.println("ERR");
  }
}

// Process "w"-write comands
void processWrite(String cmd) {
  switch (cmd[1]) {
    case 'l':
      writeLight(cmd);
      break;
    case 'e':
      writeEEPROM(cmd);
      break;
    case 'g':
      Serial.println("group:TODO");
      break;
    default:
      Serial.println("ERR W");
  }
}

// Process comand
void processCmd(char *command) {
  String cmd = command;
  Serial.println("cmd:" + cmd);
  switch (cmd[0]) {
    case 'h':
      heartBeatResponse();
      break;
    case 'r':
      processRead(cmd);
      break;
    case 'w':
      processWrite(cmd);
      break;
    case 'I':
      Serial.println("INIT");
      writeDefaultEEPROM(0);
      break;
    default:
      ledChange(0);
      Serial.println("ERR C");
  }
  sendDone();
}

// -- SHIFT 
uint32_t shift74165ReadData()
{
  long bitVal;
  uint32_t bytesVal = 0;

  /* Trigger a parallel Load to latch the state of the data lines,
  */
  digitalWrite(SHIFT_CE_P, HIGH);
  digitalWrite(SHIFT_PLOAD_P, LOW);
  delayMicroseconds(SHIFT_PULSE_WIDTH_USEC);
  digitalWrite(SHIFT_PLOAD_P, HIGH);
  digitalWrite(SHIFT_CE_P, LOW);

  /* Loop to read each bit value from the serial out line
     of the SN74HC165N.
  */
  for (int i = 0; i < BUTTON_COUNT; i++)
  {
    bitVal = digitalRead(SHIFT_DATA_P);

    /* Set the corresponding bit in bytesVal.
    */
    bytesVal |= (bitVal << ((BUTTON_COUNT - 1) - i));

    /* Pulse the Clock (rising edge shifts the next bit).
    */
    digitalWrite(SHIFT_CLOCK_P, HIGH);
    delayMicroseconds(SHIFT_PULSE_WIDTH_USEC);
    digitalWrite(SHIFT_CLOCK_P, LOW);
  }

  return (bytesVal);
}

uint32_t initShift74165() {

  long bitVal;
  uint32_t bytesVal = 0;
  for (int i = 0; i < BUTTON_COUNT; i++)
  {
    long bitVal = HIGH;

    /* Set the corresponding bit in bytesVal.
    */
    bytesVal |= (bitVal << ((BUTTON_COUNT - 1) - i));
    
  }
  return bytesVal;
}

void shift74165ProcessData() {
  //  Serial.println("Shift");
  for (int i = 0; i < BUTTON_COUNT; i++) {

    int newValue = LOW;
    int oldValue = LOW;

    if ((pinValues >> i) & 1) {
      newValue = HIGH;
    } else {
    }

    if ((oldPinValues >> i) & 1) {
      oldValue = HIGH;
      //    Serial.print("HIGH");
    } else {
      //    Serial.print("LOW");
    }

    if ( newValue == HIGH && oldValue == LOW) {
//      ledChange(i);
      chageLedGroupMap(i);
    }
  }
}

void loopShift74165() {
  pinValues = shift74165ReadData();
  if (pinValues != oldPinValues) {
    //Serial.print("*Pin value change detected*\r\n");
    shift74165ProcessData();
    oldPinValues = pinValues;
  }
  delay(SHIFT_POLL_DELAY_MSEC);

}

// -- SHIFT --

void setup() {
  Serial.begin(9600);
  //  //Serial.begin(19200);
  //  for (int i = 0; i < BUTTON_COUNT; i++) {
  //    buttons[i].attach(buttonPins[i], INPUT);
  //    buttons[i].interval(DEBOUNCE_DELAY);
  //    pinMode(ledPins[i], OUTPUT);
  //    ledDown(i);
  //  }

  /* Initialize our digital pins...
  */
  pinMode(SHIFT_PLOAD_P, OUTPUT);
  pinMode(SHIFT_CE_P, OUTPUT);
  pinMode(SHIFT_CLOCK_P, OUTPUT);
  pinMode(SHIFT_DATA_P, INPUT);

  digitalWrite(SHIFT_CLOCK_P, LOW);
  digitalWrite(SHIFT_PLOAD_P, HIGH);

  pinValues = initShift74165();

  oldPinValues = pinValues;
  pinValues = shift74165ReadData();
//  display_pin_values();

  readEEPROM(0);

  sendCompileDate();

  sendDone();

}

void checkTimer() {
  // here is where you'd put code that needs to be running all the time.

  // check to see if it's time to blink the LED; that is, if the difference
  // between the current time and last time you blinked the LED is bigger than
  // the interval at which you want to blink the LED.
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= timerInterval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;

    heartBeatEvent();

  }
}


char buf[80];

void loop() {
  //  loopDebouncers();
  loopShift74165();
  // send data only when you receive data:
  if (Serial.available() > 0) {
    if (readline(Serial.read(), buf, 80) > 0) {
      //      Serial.print("CMD:");
      //      Serial.println(buf);
      processCmd(buf);
    }

  }

  checkTimer();

}

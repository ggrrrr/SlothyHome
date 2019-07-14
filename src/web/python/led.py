import _thread
import serial
import time

tty = '/dev/ttyACM0'
tty = '/dev/tty.usbmodem2301'

rate = 9600
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port=tty,
    baudrate=rate,
    # rtscts=True,
    # dsrdtr=True,
    # parity=serial.PARITY_ODD,
    # stopbits=serial.STOPBITS_TWO,
    # bytesize=serial.SEVENBITS
)
# time.sleep(5)

ser.isOpen()
okRead = 1

def readData():
    out = []
    okRead = 0
    while ser.inWaiting() > 0:
        # print("readData.start...")
        bytesIn = ser.readline().decode("utf-8")
        line ="%s" % (bytesIn.rstrip())
        out.append(line)
        # print ( "<%s>" %  (line))
        if line == ".":
            # print("readData.stop.")
            break
    okRead = 1
    # print(out)
    return out

def readProcess(var1):
    print("readProcess...")
    done = 0
    while 1:
        if okRead:
            dataIn = readData()
            if len(dataIn) > 0:
                print("dataIn: %s" % dataIn)
        time.sleep(1)
        # print("readProcess.loop.okRead: %s" % okRead)

# readSer()

def writeSer(asd):
    ser.write(b'wlc0\r\n')
    ser.flush()
    time.sleep(0.1)

try:
    # writeSer("asd")
    _thread.start_new_thread ( readProcess, ('asd', ) )
    time.sleep(0.1)
except:
    print("unable to start thread")

# readSer(1)
try:
    while 1:
        k = input('readKey:')
        if k == '.':
            print("exit...")
            break
        else:
            okRead = 0
            print("sending:%s" % k)
            ser.write(bytes("%s\n" % k.rstrip(), 'utf-8'))
            time.sleep(0.5)
            print( "got:%s" % readData( ) )
            okRead = 1

except KeyboardInterrupt as e:
    print("ctrl+c")

ser.close()
print("done")

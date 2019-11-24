import logging
import serial
import time

class SlothyTty():
    def __init__(self, args = None,):
        self.LOG = logging.getLogger('slothyHome.tty.SlothyTty')
        self.readLines = []
        self.ttyFree = 0
        self.args = args
        self.serial = None
        self.stopLoop = 1
        self.timeSleepReadLoop = 0.5
        self.timeSleepWrite = 0.5
        self.timeSleepWriteLoop = 0.1
        self.callBack = None
        self.connect()
        self.blockEnd = "."
        self.blockStart = "cmd"
        self.blockWait = 0
        self.blocks = []

    def listDevices(self):
        out = []
        import serial.tools.list_ports
        for port in serial.tools.list_ports.comports():
            out.append({'device': port.device, 'name': port.name, 'description': port.description, 'sn': port.serial_number})
        return out


    def connect(self):
        try:
            self.serial = serial.Serial(
                port=self.args.ttyDev,
                baudrate=self.args.ttyRate,
                timeout = 0,
                # rtscts=True,
                # dsrdtr=True,
                # parity=serial.PARITY_ODD,
                # stopbits=serial.STOPBITS_TWO,
                # bytesize=serial.SEVENBITS
            )
            time.sleep(0.5)
            self.LOG.info("ttyInit: %s" % self.serial.isOpen())
            self.LOG.debug("ttyInit. %s" % self.serial )
        except IOError as e:
            self.serial = None
            self.LOG.error("connect: %s" % e )

    def readLoop(self):
        self.LOG.info("readLoop.start: %s" % ( self.serial) )
        if self.serial is None:
            self.LOG.error("readLoop: serial not connected!")
            return
        try: 
            while self.stopLoop:
                if self.ttyFree:
                    self.ttyFree = 0
                    self.readData()
                time.sleep(self.timeSleepReadLoop)
            self.LOG.debug("readLoop.end.")
        except KeyboardInterrupt:
            self.LOG.info("readLoop: KeyboardInterrupt")

    def readData(self):
        if self.serial is None:
            self.LOG.error("readData: serial not connected!")
            return
        self.LOG.debug("readData...")
        readLines = []
        if self.serial.inWaiting() > 0:
            done = 1
            line = ""
            while done:
                while self.serial.inWaiting() > 0:
                    bytesIn = self.serial.readline()
                    self.LOG.debug("GOT.BYTES:%s" % bytesIn)
                    bytesInUtf = bytesIn.decode("utf-8")
                    line = "%s%s" % (line, bytesInUtf.rstrip())
                    if '\n' in bytesInUtf:
                        readLines.append(line)
                        self.LOG.info("GOT.NL:%s" % line)
                        line = ""
                        done = 0

                    if self.blockStart in bytesInUtf:
                        self.blocks = []
                        self.blockWait = 1
                        self.LOG.info("BLOCK.START.")

                    if self.blockEnd in bytesInUtf:
                        self.blocks.append(readLines)
                        self.blockWait = 0
                        self.LOG.info("BLOCK.END:%s" % readLines)

        if len(readLines) > 0:
            self.LOG.info("readData.readLines:%s" % ( readLines))


        self.ttyFree = 1
        if len(readLines) > 0:
            self.LOG.info("readData.data:%s" % ( readLines))
            if self.callBack is not None:
                self.LOG.info("readData.data: callBack:%s: %s" % (self.callBack.__name__, readLines))
                self.callBack(self.mqtt, readLines)
        return readLines

    def sendDataWait(self, data):
        while 1:
            if self.ttyFree:
                try:
                    self.serial.write(bytes("%s\n" % data, 'utf-8'))
                    self.LOG.info("sendDataWait:data:%s" % (data) )
                    time.sleep(self.timeSleepWrite)
                except IOError as e:  
                    self.LOG.error("sendDataWait:data:%s" % (e) )
                    return False

                break
            time.sleep(self.timeSleepWriteLoop)
        self.ttyFree = 1
        return self.readData()

    def sendData(self, data):
        if self.serial is None:
            self.LOG.error("sendData: serial not connected!")
            return False
        while 1:
            if self.ttyFree:
                try:
                    self.serial.write(bytes("%s\n" % data, 'utf-8'))
                    self.LOG.info("sendData:data:%s" % (data) )
                    time.sleep(self.timeSleepWrite)
                    return True
                except IOError as e:  
                    self.LOG.error("sendData:data:%s" % (e) )
                    return False

                break
            time.sleep(self.timeSleepWriteLoop)

    def close(self):
        self.LOG.info("close...")
        self.serial.close()
        self.LOG.info("close:%s" % self.serial)

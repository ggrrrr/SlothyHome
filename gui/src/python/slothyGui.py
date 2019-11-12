from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

import paho.mqtt.client as mqtt
import requests
import argparse
import logging
import time

logging.basicConfig(level=logging.DEBUG)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("on_connect: %s %s, %s" %(  client, userdata, msg, ))
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info("on_message:client:%s, userdata:%s, topic:%s, message:%s" %(  client, userdata, msg.topic, msg.payload ))
    print(msg.topic+" "+str(msg.payload))

def pushSwitch():
    try:
        response = requests.get("%s%s" % ( args.domoticz, "/json.htm?type=command&param=switchlight&idx=1&switchcmd=Toggle") )
        if ( response.status_code == 200):
            json = response.json()
            data = json['status']
            # messagebox.showinfo("Information",data)
        else:
            messagebox.showerror("Error","error:%s" % response.status_code)
    except BaseException as e:
        messagebox.showerror("Error","%s" % e)

def getTemp():
    try:
        response = requests.get("%s%s" % ( args.domoticz, "/json.htm?type=devices&rid=2") )
        if ( response.status_code == 200):
            json = response.json()
            data = json['result'][0]['Data']
            return data
        else:
            return "error:%s" % response.status_code
    except:
        return "error"



def quit(*args):
	root.destroy()

def fetchData(root):
    root.txtTime.set(time.strftime("%H:%M:%S"))
    root.txtTemp.set(getTemp())
    root.after(1000, fetchData, root)

def Gui(args):
    root = Tk()
    if args.full is not None:
        root.attributes("-fullscreen", True)
        root.configure(xbackground='black')
        root.bind("<Escape>", quit)
        root.bind("x", quit)
    else:
        root.geometry('800x600')
        root.title("Slothy Home UI")

    fnt = font.Font(family='Helvetica', size=12, weight='bold')

    txtTime = StringVar()
    txtTime.set(time.strftime("%H:%M:%S"))

    txtTemp = StringVar()
    txtTemp.set("n/a")

    # root.after(1000, fetchData, root)

    lblTime = ttk.Label(root, textvariable=txtTime, font=fnt, foreground="green", background="black")
    # lblTime.place(relx=0.5, rely=0.5, anchor=NE)
    lblTime.grid(column=0, row=0)

    lblTemp = ttk.Label(root, textvariable=txtTemp, font=fnt, foreground="green", background="black")
    # lblTemp.place(relx=0.5, rely=0.5, anchor=NE)
    lblTemp.grid(column=0, row=1)

    lbl = ttk.Label(root, text="some shit", font=fnt)
    lbl.grid(column=0, row=2)

    ttk.Button(root, text="MyLed", command=pushSwitch).grid(column=3, row=3, sticky=W)

    root.mainloop()

def mqttInit(args):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(args.mqttHost, 1883, 60)
    client.subscribe(args.mqttTopic)
    client.loop_start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='slothy GUI.')
    #parser.add_argument('--hosts', default=None, dest='hosts', help='host')
    parser.add_argument('--full', default=None, dest='full', help='full screen')
    parser.add_argument('--domoticz', default="http://192.168.88.235:8080", dest='domoticz', help='domoticz url')
    parser.add_argument('--mqttHost', default="192.168.88.235", dest='mqttHost', help='Mqtt host')
    parser.add_argument('--mqttTopic', default="test", dest='mqttTopic', help='Mqtt topic')

    args = parser.parse_args()

    # mqttInit(args)

    Gui(args)

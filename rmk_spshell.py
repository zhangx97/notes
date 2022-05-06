#pi@raspberrypi:~ $ cat .rmkcfg/rmk_spshell.py
# -*- coding: utf8 -*-
#!/usr/bin/python

import serial, signal
import serial.tools.list_ports as port_list

def enmuerate_serial_port():
    port = list(port_list.comports())
    for i in range(len(port)):
        try:
            yield list(port[i])[0]
        except EnvironmentError:
            break

def com_search_open():
    global ser, BaudRate, SerialTimeout, connected, serialName

    if serialName == "null" or serialName == "":
        return

    try:
        ser = serial.Serial(serialName, BaudRate, timeout = SerialTimeout)
        header = ser.readline()
        if 'Start' in header:
            header=ser.readline()
            if 'Dev Init OK' in header:
                connected = True
                print 'connect'
    except Exception, e:
        print str(e)

def SplitFile(readLines, name):
    for i in readLines:
        if name in i:
            return i.split()

def getConfig():
    global BaudRate, SerialTimeout, serialName

    fileconf = "/home/pi/python_project/RealMakerConfig.ini"

    f_ini = open(fileconf, "r")
    readLines = f_ini.readlines()

    BaudRate = int(SplitFile(readLines, 'BaudRate')[1])
    SerialTimeout = int(SplitFile(readLines, 'SerialTimeOut')[1])
    serialName = SplitFile(readLines, 'DevSerial')[1]

class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    raise AlarmException

def raw_input_timeout(timeout=30):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)

    try:
        astring = raw_input()
        signal.alarm(0)
        return astring
    except AlarmException:
        print "timeout"
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return

def motorStepper():
    global ser

    while True:
        cmd = raw_input_timeout(300)
        #print cmd
        if cmd == '' or cmd == None:
            break

        send_cmd = cmd + '\n'
        ser.write(send_cmd)
        print ser.readline()[0:-2]
        ack = ser.readline()[0:-2]
        print ack
        if "ER" in ack or "X:" in ack:
            print ser.readline()[0:-2]

if __name__ == "__main__":
    getConfig()
    com_search_open()
    motorStepper()

#!/usr/bin/env python3
import serial
import time

#before running install pyserial library -yunas
#python3 -m pip install pyserial 

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        command = str.encode(input())
        ser.write(b"%s\n" % command)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

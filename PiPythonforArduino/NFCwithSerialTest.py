#!/usr/bin/env python3
import serial
import time
import RPi.GPIO as GPIO
from pn532 import *

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        
        try:
            #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
            #pn532 = PN532_I2C(debug=False, reset=20, req=16)
            pn532 = PN532_UART(debug=False, reset=20)

            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()

            print('Waiting for RFID/NFC card...')
            while True:
                # Check if a card is available to read
                uid = pn532.read_passive_target(timeout=0.5)
                print('.', end="")
                # Try again if no card is available.
                if uid is None:
                    continue
                print('Found card with UID:', [hex(i) for i in uid])
                #command = str.encode(uid)
                command = [hex(i) for i in uid]
                ser.write(b"%s\n" % command)
                ##ser.write(b"test phrase\n")
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
        except Exception as e:
            print(e)
        finally:
            GPIO.cleanup()

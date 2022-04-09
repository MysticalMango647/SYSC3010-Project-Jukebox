'''
This script runs on the Jukebox Pi and test that communication between the Pi and Arduino is working correctly
Written by: Corbin Garlough
'''
#!/usr/bin/env python3
# imports
import serial
import time

if __name__ == '__main__':
    
    # initialize serial communication with Arduino
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    
    while True:
        # send a test string to the Arduino over UART
        teststring = "updateDisplay(some text)\n"
        ser.write(teststring.encode('utf-8'))
        
        #recieve the reply to make sure the string sent was read correctly
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

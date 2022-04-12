
import serial
import time


def write_read(x):
    arduino = serial.Serial(port='COM7', baudrate=115200, timeout=0.1)
    #arduino.write(bytes(x, 'utf-8'))
    arduino.write(x.encode('utf-8'))
    time.sleep(0.05)
    #data = arduino.readline()
    data1 = arduino.readline().decode('utf-8').rstrip()
    str(data1)
    return data1


if __name__ == '__main__':
    while True:
        songfullname = input("Enter the function: ")  # Taking input from user
        returnData = write_read(songfullname)
        print(returnData)





import serial
import time



def write_read(x):
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    arduino.reset_input_buffer()
    #arduino.write(bytes(x, 'utf-8'))
    #arduino.write(x.encode('utf-8'))
    arduino.write(b"1,2,\n")
    
    time.sleep(2)
    #data = arduino.readline()
    data1 = arduino.readline().decode('utf-8').rstrip()
    str(data1)

    return data1


# if __name__ == '__main__':
#     # while True:
#     #     songfullname = input("Enter the function: ")  # Taking input from user
#     #     returnData=write_read(songfullname)
#     #     print(returnData)
#     #
#     #     #print(song)
# 
#     ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#     ser.reset_input_buffer()
#     while True:
#         ser.write(b"Hello from Raspberry Pi!\n")
#         line = ser.readline().decode('utf-8').rstrip()
#         print(line)
#         time.sleep(1)


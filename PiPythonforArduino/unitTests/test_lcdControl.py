import unittest
#from lcdControl import write_read
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
    print(data1)

    return data1

class testLCD(unittest.TestCase):
    def test_input(self):
        test1 = write_read("1,2,\n")
        test2 = write_read("Line1,Line2,\n")
        print(test1 + "here t1")
        print(test2 + "here t2")
        self.assertEqual(test1, '1,2,')
        self.assertEqual(test2, 'Line1,Line2,')

if __name__ == "__main__":
    unittest.main()
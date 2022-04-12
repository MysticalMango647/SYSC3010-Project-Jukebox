import unittest
from lcdControl import write_read

import serial
import time


class testLCD(unittest.TestCase):
    def test_input(self):
        test1 = write_read("1,2,")
        test2 = write_read("Line1,Line2,")
        print(test1 + "here test1")
        print(test2 + "here test2")
        self.assertNotEqual(test1, '1,2,')
        self.assertNotEqual(test2, 'Line1,Line2,')



if __name__ == "__main__":
    unittest.main()
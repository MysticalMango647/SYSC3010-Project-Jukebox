import RPi.GPIO as GPIO
from pn532 import *
import serial
import unittest

GPIO.setwarnings(False)

def readTagID():
    try:
        #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        #print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()
        
        
        cardIDprev = ""

        #print('Waiting for RFID/NFC card...')
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            cardID = ""
            i=0
            while i < 4:
                cardID = cardID + str(uid[i])
                i += 1
            if cardID != cardIDprev:
                #print("\n" + cardID)
                return cardID
            cardIDprev = cardID
#             for i in tagIDs:
#                 print("Key: " + i.key())
#                 print("Val: " + i.val())
#                 if i.key() == cardID:
#                     print("tag in db")
            
            #print('Found card with UID:', [hex(i) for i in uid])
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
        
        
class TestNFCMethods(unittest.TestCase):

    def test_NFCRead(self):
        tagID = readTagID()
        self.assertEqual(tagID, '13569103')
        
def main():
    print("\n" + readTagID())
  
if __name__ == "__main__":
    unittest.main()
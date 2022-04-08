#imports
import RPi.GPIO as GPIO
from pn532 import *
import serial
import unittest

#disable GPIO warnings
GPIO.setwarnings(False)

'''
readTagID() reads an NFC tag ID and returns its value
@return cardID the ID of the scanned tag
'''
def readTagID():
    try:
        #initialize NFC reader
        pn532 = PN532_UART(debug=False, reset=20)
        ic, ver, rev, support = pn532.get_firmware_version()
        
        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()
        
        cardIDprev = ""

        # wait for a card to be detected
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            cardID = ""
            i=0
            # decode the hexidecimal value
            while i < 4:
                cardID = cardID + str(uid[i])
                i += 1
            # if the card scanned is different from the last card, send the new tag ID
            if cardID != cardIDprev:
                return cardID
            # update the ID of the last scanned card
            cardIDprev = cardID
            
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
        
        
class TestNFCMethods(unittest.TestCase):
    '''
    test_NFCRead() tests to make sure a known tag will produce a known ID when scanned
    '''
    def test_NFCRead(self):
        # read a tag ID
        tagID = readTagID()
        
        # make sure the decoded ID matches what the known ID of the tag is
        self.assertEqual(tagID, '13569103')
  
if __name__ == "__main__":
    unittest.main()

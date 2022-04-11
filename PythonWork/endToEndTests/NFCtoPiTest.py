'''
This script runs on the Jukebox Pi and tests that the NFC scanner is working correctly and generating the correct ID for a known tag
Written by: Corbin Garlough
'''

#imports
import RPi.GPIO as GPIO
from pn532 import *
import serial
import unittest

#disable GPIO warnings
GPIO.setwarnings(False)

'''
readTagID() waits for an NFC tag to be held within range of the scanner and
then returns the tags ID
@return cardID the ID of the tag just scanned
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
            
            # decode hexidecimal tag ID
            while i < 4:
                cardID = cardID + str(uid[i])
                i += 1
                
            # if the card scanned is a new card, then return the cardID
            if cardID != cardIDprev:
                return cardID
            
            #update the last scanned card ID
            cardIDprev = cardID
            
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
        
        
class TestNFCMethods(unittest.TestCase):
    '''
    test_NFCRead() makes sure that a known tag is read properly, and produces the correct tag ID
    '''
    def test_NFCRead(self):
        # read a tag ID
        tagID = readTagID()
        
        #make sure the tag produces the expected ID
        self.assertEqual(tagID, '13569103')
        
def main():
    print("\n" + readTagID())
  
if __name__ == "__main__":
    unittest.main()

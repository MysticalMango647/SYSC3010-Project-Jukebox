import pyrebase
import random
import time
from sense_hat import SenseHat
from datetime import datetime
import RPi.GPIO as GPIO
from pn532 import *
import serial

GPIO.setwarnings(False)

# Create new Firebase config and database object
config = {
  "apiKey": "AIzaSyBKzE2PdUDJzSC0KE_NxESoElAExzbLTv8",
  "authDomain": "ijukebox-8f5bd.firebaseapp.com",
  "databaseURL": "https://ijukebox-8f5bd-default-rtdb.firebaseio.com/",
  "storageBucket": "ijukebox-8f5bd.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

dataset1 = "tagIDs"
  
def readData():
  # Returns the entry as an ordered dictionary (parsed from json)
  tagIds = db.child(dataset1).get()
 
  #print("Parent Key: {}".format(tagIds.key()))
 
  # Returns the dictionary as a list
  tagIds_list = tagIds.each()
  # Takes the last element of the list
  #tagIdslastDataPoint = tagIds_list[-1]
 
  #print("Child Key: {}".format(tagIdslastDataPoint.key()))
  #print("Child Value: {}\n".format(tagIdslastDataPoint.val()))
#   for i in tagIds_list:
#       print("Key: " + i.key())
#       print("Val: " + i.val())
#   if "test" in tagIds_list:
#       print("Test in list")
  return tagIds_list
def readTagID(tagIDs):
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
                print("\n" + cardID)
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

def updateDisplay(cardID, ser, tagIDs):
    for i in tagIDs:
#         print("Key: " + i.key())
#         print("Val: " + i.val())
        if i.key() == cardID:
            teststring = "updateDisplay(" + i.val() + ")\n"
    #teststring = "updateDisplay(" + cardID + ")\n"
    ser.write(teststring.encode('utf-8'))
    time.sleep(1)
    line = ser.readline().decode('utf-8').rstrip()
    time.sleep(1)
    print(line)
    
def main():
    tagIDs = readData()
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        updateDisplay(readTagID(tagIDs), ser, tagIDs)
  
if __name__ == "__main__":
    main()
    


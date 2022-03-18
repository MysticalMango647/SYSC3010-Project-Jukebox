import pyrebase
import random
import time
from sense_hat import SenseHat
from datetime import datetime
import RPi.GPIO as GPIO
from pn532 import *
import serial
import sqlite3
from datetime import date

debug = True

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
dataset2 = "songRequests"

#connect to database file
dbconnect = sqlite3.connect("iJukeboxDB");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();

def getTags():
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
                print("\nTag ID: " + cardID)
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

def updateDisplay(message, ser):
    teststring = ""
    
    teststring = "updateDisplay(" + message + ")\n"
    ser.write(teststring.encode('utf-8'))
    time.sleep(2)
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    
def getCardVal(cardID, tagIDs):
    for i in tagIDs:
#         print("Key: " + i.key())
#         print("Val: " + i.val())
        if i.key() == cardID:
            infoPair = i.val().split(',', 1)
            print ("Song: " + infoPair[0])
            print ("Artist: " + infoPair[1])
            
            return infoPair
            
def logRequest(info, key):
    key = key
 
  #while True:
    # I'm using dummy sensor data here, you could use your senseHAT
    #edit test
    time = str(datetime.now().time())
    strippedTime = time.split('.', 1)[0]
    currDate = date.today()
    
    

    # Will be written in this form:
    # {
    #   "sensor1" : {
    #     "0" : 0.6336863763908736,
    #     "1" : 0.33321038818190285,
    #     "2" : 0.6069185320998802,
    #     "3" : 0.470459178006184,
    #   }
    # }
    # Each 'child' is a JSON key:value pair
    if debug == True:
        print("Time: " + strippedTime)
        print("Date: " + str(currDate))
        print("Info logged: " + info[0] + "," + info[1])

    db.child(dataset2).child(currDate).child(strippedTime).set(info)

    #time.sleep(5)
    
def logRequestLocal(info):
    #execute insert statement
    song = info[0]
    artist = info[1]
    album = "NONE"
    currtime = str(datetime.now().time())
    strippedTime = currtime.split('.', 1)[0]
    cursor.execute('''insert into songRequests values (date('now'), ?, ?, ?, ?)''', (strippedTime, song, artist, album));
    dbconnect.commit();
    time.sleep(1);
    
    
def main():
    i = 1
    tagIDs = getTags()
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    prevTagID = ""
    while True:
        tagID = readTagID(tagIDs)
        if tagID != prevTagID:
            tagVal = getCardVal(tagID, tagIDs)
            try:
                message = tagVal[0] + "," + tagVal[1]
                updateDisplay(message, ser)
                prevTagID = tagID
                logRequest(tagVal, i)
                logRequestLocal(tagVal)
                i += 1
            except:
                print("Invalid Tag ID")
    #close the connection
    dbconnect.close();
            
  
if __name__ == "__main__":
    main()
    


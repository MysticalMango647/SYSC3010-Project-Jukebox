'''
Flake8 output:
Desktop/SYSC3010/SYSC3010-Project-Jukebox/PiPythonforArduino/DBtest.py:24:1:
F403 'from pn532 import *' used; unable to detect undefined names
Desktop/SYSC3010/SYSC3010-Project-Jukebox/PiPythonforArduino/DBtest.py:82:17:
F405 'PN532_UART' may be undefined, or defined from star imports: pn532

I am unsure of what is wrong with the pn532 import but it works as normal, so
I did not address the issue.

This program is meant to simulate a Jukebox that is capable of playing songs
from reading an NFC tag. The program will scan an NFC tag, go into a Firebase
database and find the corresponding song and artist info for a given tag ID,
update a screen on a connected arduino with the song and artist name, and
log the song request info in both a Firebase database and a local database.
'''


# import all used libraries
import pyrebase
import time
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

# define the names of tables used in Firebase database
dataset1 = "tagIDs"
dataset2 = "songRequests"

# connect to a local database file
dbconnect = sqlite3.connect("iJukeboxDB")
dbconnect.row_factory = sqlite3.Row
cursor = dbconnect.cursor()

'''
getTags() goes into the firebase database and gets the current set of all
used NFC tag IDs.
@return tagIds_list a list of currently stored tag IDs
'''


def getTags():
    # Returns the entry as an ordered dictionary (parsed from json)
    tagIds = db.child(dataset1).get()

    # converts the dictionary to a list
    tagIds_list = tagIds.each()

    return tagIds_list


'''
readTagID() waits for an NFC tag to be held within range of the scanner and
then returns the tags ID
@return cardID the ID of the tag just scanned
'''


def readTagID():
    try:
        # Initialize the UART communication interface for the PN532
        # pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        # pn532 = PN532_I2C(debug=False, reset=20, req=16)
        pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()

        # Configure PN532 to communicate with MiFare NFC cards
        pn532.SAM_configuration()

        # variable to hold previously scanned tag so that if the same
        # tag is scanned twice, the system will ignore repeat scans
        cardIDprev = ""

        # loop to wait for tag to be scanned
        while True:
            # Check if a tag is available to read
            uid = pn532.read_passive_target(timeout=0.5)

            print('.', end="")

            # Try again if no tag is available.
            if uid is None:
                continue

            # variable to hold scanned tag ID
            cardID = ""
            i = 0

            # parse read tag ID and convert to decimal value
            while i < 4:
                cardID = cardID + str(uid[i])
                i += 1

            # if the tag scanned is a new tag, return the tag ID
            if cardID != cardIDprev:
                print("\nTag ID: " + cardID)
                return cardID

            # update previously scanned tag
            cardIDprev = cardID

    # handling for unexpected events
    except Exception as e:
        print(e)

    finally:
        GPIO.cleanup()


'''
updateDisplay() sends a message to the connected Arduino to
display a message on the LCD display
@param message the text to display with the first and second line's
       text separated with a ','
@param ser the serial connection to the Arduino
'''


def updateDisplay(message, ser):
    # message to display
    teststring = ""
    teststring = message

    # write message to serial connection
    ser.write(teststring.encode('utf-8'))
    time.sleep(2)

    # get response from Arduino that it has updated screen
    line = ser.readline().decode('utf-8').rstrip()
    print(line)


'''
getCardVal() goes into the Firebase database and looks up the
corresponding song info for a tag ID it gets passed
@param cardID NFC tag ID of a scanned card
@param tagIDs a list of all currently stored tag IDs
@return infoPair the set of song title and artist name associated
        with the passed tag ID
'''


def getCardVal(cardID, tagIDs):
    # iterate through the list of tag ID to find the one matching
    # the passed value
    for i in tagIDs:

        # when a matching value if found get its corresponding
        # song and artist info
        if i.key() == cardID:
            infoPair = i.val().split(',', 1)
            print("Song: " + infoPair[0])
            print("Artist: " + infoPair[1])

            return infoPair


'''
logRequest() logs a song play request in the Firebase database,
including the data and time it was requested, the song name, and
artist name
@param info the song and artist name of the song requested
@param key a key for the Firebase database to tell what number
       entry is being made
'''


def logRequest(info, key):
    key = key

    # get the data and time that the request was made
    time = str(datetime.now().time())
    strippedTime = time.split('.', 1)[0]
    currDate = date.today()

    # debugging info
    if debug:
        print("Time: " + strippedTime)
        print("Date: " + str(currDate))
        print("Info logged: " + info[0] + "," + info[1])

    # create a new entry in the Firebase database for the request at
    # the correct time
    db.child(dataset2).child(currDate).child(strippedTime).set(info)


'''
logRequestLocal() logs a song play request in the local database,
including the data and time it was requested, the song name, and
artist name
@param info the song and artist name of the song requested
'''


def logRequestLocal(info):

    # separating info into its components
    song = info[0]
    artist = info[1]
    album = "NONE"

    # get the date and time the request was made
    currtime = str(datetime.now().time())
    strippedTime = currtime.split('.', 1)[0]

    # execute insert statement to create entry in the database
    cursor.execute('''insert into songRequests values (date('now'),
                    ?, ?, ?, ?)''', (strippedTime, song, artist, album))
    dbconnect.commit()
    time.sleep(1)


'''
main function of the sytem
'''


def main():
    # start counting how many entries are made into the Firebase database
    i = 1

    # get the list of all stored tag IDs
    tagIDs = getTags()

    # initilize the serial communication
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    # create variable to store the last scanned tag ID
    prevTagID = ""

    while True:
        # read a tag ID
        tagID = readTagID(tagIDs)

        # if the tag ID is a new tag begin processing the request
        if tagID != prevTagID:

            # fetch the song and artist info from the Firebase database
            # using the tag ID
            tagVal = getCardVal(tagID, tagIDs)
            try:
                # format the message to display on the LcD screen
                message = tagVal[0] + "," + tagVal[1] + ","

                # update display with message
                updateDisplay(message, ser)

                # store the tag ID as the last scanned tag
                prevTagID = tagID

                # log the request in the Firebase database
                logRequest(tagVal, i)

                # log the request in the local database
                logRequestLocal(tagVal)

                # increment number of logs made
                i += 1

            # an invalid tag ID was found
            except Exception:
                print("Invalid Tag ID")

    # close the connection to the database
    dbconnect.close()

# run the main function on program start


if __name__ == "__main__":
    main()

'''
This script runs on the Jukebox Pi and makes sure that the Pi is able to log a request
in the Firebase database with the information in the proper format, and checks to make
sure when a known tag ID is passed that the correct song info is retrieved from the database.
Written by: Corbin Garlough
'''
# imports
import pyrebase
import random
import time
from datetime import datetime
import RPi.GPIO as GPIO
from pn532 import *
import serial
import sqlite3
from datetime import date
import unittest

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

'''
getRequests() gets an updated list of play requests made
@return request_list a list of all requests
'''
def getRequests():
  # Returns the entry as an ordered dictionary (parsed from json)
  requests = db.child(dataset2).get()
  
  # Returns the dictionary as a list
  request_list = requests.each()
 
  return request_list
    
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
 
    # getting the time the request was made
    time = str(datetime.now().time())
    strippedTime = time.split('.', 1)[0]
    currDate = date.today()

    # log the request
    db.child(dataset2).child(currDate).child(strippedTime).set(info)
    
'''
getCardVal() goes into the Firebase database and looks up the
corresponding song info for a tag ID it gets passed
@param cardID NFC tag ID of a scanned card
@param tagIDs a list of all currently stored tag IDs
@return infoPair the set of song title and artist name associated
        with the passed tag ID
'''
def getCardVal(cardID, tagIDs):
    for i in tagIDs:
#         print("Key: " + i.key())
#         print("Val: " + i.val())
        if i.key() == cardID:
            infoPair = i.val().split(',', 1)
            print ("Song: " + infoPair[0])
            print ("Artist: " + infoPair[1])
            
            return infoPair
'''
getTags() goes into the firebase database and gets the current set of all
used NFC tag IDs.
@return tagIds_list a list of currently stored tag IDs
'''    
def getTags():
  # Returns the entry as an ordered dictionary (parsed from json)
  tagIds = db.child(dataset1).get()
  
  # Returns the dictionary as a list
  tagIds_list = tagIds.each()
  return tagIds_list

class TestNFCMethods(unittest.TestCase):

    '''
    test_FirebaseWrite() makes sure that when a request is logged in the Firebase database, that the info is in the correct format.
    Also it checks to make sure when a known tag value is passed, the info returned by the lookup corresponds to the correct song and artist.
    '''
    def test_FirebaseWrite(self):
        # create a dummy test request
        tagVal = ["test song", "test artist"]
        
        # log the request
        logRequest(tagVal, 1)
        
        nowtime = str(datetime.now().time())
        nowstrippedTime = nowtime.split('.', 1)[0]
        todayDate = date.today()
        
        # get an updated list of requests
        requests = db.child(dataset2).child(todayDate).child(nowstrippedTime).get()
        
        # make sure that the test request was logged properly
        self.assertEqual(requests[0].val(), 'test song')
        self.assertEqual(requests[1].val(), 'test artist')
        
        # get updated list of all tags present in the system
        tags = getTags()
        
        # retrieve the info corresponding to the passed tag ID
        info = getCardVal("13569103", tags)
        
        # make sure the info is as expected
        self.assertEqual(info[0], "Sink The Pink")
        self.assertEqual(info[1], "ACDC")
        
  
if __name__ == "__main__":
    unittest.main()
    



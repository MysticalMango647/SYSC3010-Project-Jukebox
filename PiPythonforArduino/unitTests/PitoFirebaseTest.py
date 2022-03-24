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

def getRequests():
  # Returns the entry as an ordered dictionary (parsed from json)
  requests = db.child(dataset2).get()
  
  # Returns the dictionary as a list
  request_list = requests.each()
 
  return request_list
    
def logRequest(info, key):
    key = key
 
    time = str(datetime.now().time())
    strippedTime = time.split('.', 1)[0]
    currDate = date.today()

    db.child(dataset2).child(currDate).child(strippedTime).set(info)
    
def getCardVal(cardID, tagIDs):
    for i in tagIDs:
#         print("Key: " + i.key())
#         print("Val: " + i.val())
        if i.key() == cardID:
            infoPair = i.val().split(',', 1)
            print ("Song: " + infoPair[0])
            print ("Artist: " + infoPair[1])
            
            return infoPair
    
def getTags():
  # Returns the entry as an ordered dictionary (parsed from json)
  tagIds = db.child(dataset1).get()
  
  # Returns the dictionary as a list
  tagIds_list = tagIds.each()
  return tagIds_list

class TestNFCMethods(unittest.TestCase):

    def test_FirebaseWrite(self):
        tagVal = ["test song", "test artist"]
        logRequest(tagVal, 1)
        nowtime = str(datetime.now().time())
        nowstrippedTime = nowtime.split('.', 1)[0]
        todayDate = date.today()
        requests = db.child(dataset2).child(todayDate).child(nowstrippedTime).get()
        #print(requests[0].val())
        self.assertEqual(requests[0].val(), 'test song')
        self.assertEqual(requests[1].val(), 'test artist')
        tags = getTags()
        info = getCardVal("13569103", tags)
        self.assertEqual(info[0], "Sink The Pink")
        self.assertEqual(info[1], "ACDC")
        
  
if __name__ == "__main__":
    unittest.main()
    



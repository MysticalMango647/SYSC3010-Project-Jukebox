# imports
import pyrebase
import random
import time
from sense_hat import SenseHat
from datetime import datetime
import RPi.GPIO as GPIO
import serial
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
'''
readData() goesto the firebase database and retrieves an updated list of all stored tag IDs
'''
def readData():
  # Returns the entry as an ordered dictionary (parsed from json)
  tagIds = db.child(dataset1).get()
  
  # Returns the dictionary as a list
  tagIds_list = tagIds.each()
    
  return tagIds_list

class TestFirebaseMethods(unittest.TestCase):
    '''
    test_FirbaseRead() makes sure the system is able to read data from the firebase database
    '''
    def test_FirbaseRead(self):
        # get an updated list of all stored tag IDs
        tagIDs = readData()
        
        #make sure the first stored ID is for a test tag
        self.assertEqual(tagIDs[0].val(), 'test')

def main():
    tagIDs = readData()
  
if __name__ == "__main__":
    unittest.main()

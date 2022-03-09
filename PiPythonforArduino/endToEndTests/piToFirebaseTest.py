import pyrebase
import random
import time
from sense_hat import SenseHat
from datetime import datetime
import RPi.GPIO as GPIO
import serial

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
  
  # Returns the dictionary as a list
  tagIds_list = tagIds.each()
  
  for i in tagIds:
    print("Key: " + i.key())
    print("Val: " + i.val())
    
  return tagIds_list

def main():
    tagIDs = readData()
  
if __name__ == "__main__":
    main()
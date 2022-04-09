'''
This script runs on the Jukebox Pi and tests to make sure that the Pi is 
able to log requests with info in the proper format in the local database.
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

#connect to database file
dbconnect = sqlite3.connect("/home/pi/Desktop/SYSC3010/SYSC3010-Project-Jukebox/PiPythonforArduino/iJukeboxDB");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();

'''
getRequests() gets an updated list of play requests made
@return requests a list of all requests
'''
def getRequests():
  # Returns the entry as an ordered dictionary (parsed from json)
  requestData = cursor.execute('SELECT * FROM songRequests');
  
  requests = requestData.fetchall()
 
  return requests

'''
logRequestLocal() logs a song play request in the local database,
including the data and time it was requested, the song name, and
artist name
@param info the song and artist name of the song requested
'''
def logRequestLocal(info):
   # breakdown the info into its components
    song = info[0]
    artist = info[1]
    
    album = "NONE"
    
    #get the time the request was made
    currtime = str(datetime.now().time())
    strippedTime = currtime.split('.', 1)[0]
    
    # execute insert statement
    cursor.execute('''insert into songRequests values (date('now'), ?, ?, ?, ?)''', (strippedTime, song, artist, album));
    dbconnect.commit();
    time.sleep(1);
    
class TestNFCMethods(unittest.TestCase):
    '''
    test_localDBWrite() makes sure that when a request is logged in the local database, that the info is in the correct format.
    '''
    def test_localDBWrite(self):
        # create a dummy test request
        tagVal = ["test song", "test artist"]
        
        # get the time the request was made
        nowtime = str(datetime.now().time())
        nowstrippedTime = nowtime.split('.', 1)[0]
        
        # log the request
        logRequestLocal(tagVal)
        
        # get updated list of all requests logged
        requests = getRequests()
        
        # ensure the logged data matches what was expected
        self.assertEqual(requests[-1][1], nowstrippedTime)
        self.assertEqual(requests[-1][2], 'test song')
        self.assertEqual(requests[-1][3], 'test artist')
        
def main():
    getRequests()
  
if __name__ == "__main__":
    unittest.main()
    #main()
    




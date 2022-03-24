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

def getRequests():
  # Returns the entry as an ordered dictionary (parsed from json)
  requestData = cursor.execute('SELECT * FROM songRequests');
  
  requests = requestData.fetchall()
 
  return requests
    
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
    
class TestNFCMethods(unittest.TestCase):

    def test_localDBWrite(self):
        tagVal = ["test song", "test artist"]
        nowtime = str(datetime.now().time())
        nowstrippedTime = nowtime.split('.', 1)[0]
        logRequestLocal(tagVal)
        requests = getRequests()
        self.assertEqual(requests[-1][1], nowstrippedTime)
        self.assertEqual(requests[-1][2], 'test song')
        self.assertEqual(requests[-1][3], 'test artist')
        
def main():
    getRequests()
  
if __name__ == "__main__":
    unittest.main()
    #main()
    




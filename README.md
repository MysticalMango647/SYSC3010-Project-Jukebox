# iJukebox  
SYSC 3010 A   
Group L3-G6: Corbin Garlough, Yunas Magsi, Flynn Graham  
TA: Roger Selzler  
![Project Image](finishedProduct.PNG)
___

## Project Summary  
The iJukebox is a miniature Jukebox that sits in a common area, its main function is to read NFC cards and play songs while displaying the cover art of the song being played. These NFC cards are decorated with the artist’s album cover and store values for songs from a specific artist. When a user picks a song they like, they will insert their card in the iJukebox and it will scan the NFC card to place a request for that song to play from Spotify. The iJukebox reads NFC cards, fetches a corresponding song’s info from a Firebase database based on an ID read from the NFC tag, updates a display with the song info, and plays the song on a separate speaker. 

## Repo Description
Our project repo is made up of directories for the Python, Arduino, and web app code that is required to make the iJukebox work. We also have a directory for our WIPURs, and an image of the final iJukebox product. In the PythonWork directory you will find folders for the end to end, and unit tests for the system, the support files needed for the PN 532 NFC reader, the local database that we use to store play requests (iJukeboxDB), and the main program to run on the jukebox Pi (jukeboxMain.py). (FINISH SUMMARY OF ARDUINO FOLDER). (FINISH SUMMARY OF WEB APP FOLDER).

## Installation Instructions

## How to run the system
### Jukebox Pi
To get the jukebox Pi part of the system operational, open the jukeboxMain.py to make a few edits based on your specific information. First, on line 30 enter your email account you would like notifications to be sent to (right now the notifications only work with Gmail accounts). Next on line 307, change the IP address used in the post request to that of the Speaker Pi you are using. Now you can run this program, and once the other components are started, the iKukebox Pi is ready to rock out!

### Speaker Pi

### Arduinos





### **References**  
-  [Installing arduino IDE](https://electropeak.com/learn/install-arduino-ide-on-raspberry-pi/#:~:text=Download%20the%20Arduino%20software%20for%20Linux%20operating%20systems%20based%20on%20ARM%20processors.&text=Right%2Dclick%20on%20the%20file%20and%20select%20Extract%20Here.&text=Double%20click%20on%20install.sh,Execute%20or%20Execute%20in%20Terminal)
-  [Serial communication between Arduino and Pi](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/)  
-  [NFC communication](https://www.raspberrypi.com/news/read-rfid-and-nfc-tokens-with-raspberry-pi-hackspace-37/)

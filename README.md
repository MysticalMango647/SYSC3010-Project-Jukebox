# iJukebox  
SYSC 3010 A   
Group L3-G6: Corbin Garlough, Yunas Magsi, Flynn Graham  
TA: Roger Selzler  
![Project Image](finishedProduct.PNG)
___

## Project Summary  
The iJukebox is a miniature Jukebox that sits in a common area, its main function is to read NFC cards and play songs while displaying the cover art of the song being played. These NFC cards are decorated with the artist’s album cover and store values for songs from a specific artist. When a user picks a song they like, they will insert their card in the iJukebox and it will scan the NFC card to place a request for that song to play from Spotify. The iJukebox reads NFC cards, fetches a corresponding song’s info from a Firebase database based on an ID read from the NFC tag, updates a display with the song info, and plays the song on a separate speaker. 

## Repo Description
Our project repo is made up of directories for the Python, Arduino, and web app code that is required to make the iJukebox work. We also have a directory for our WIPURs, and an image of the final iJukebox product. In the PythonWork directory you will find folders for the end to end, and unit tests for the system, the support files needed for the PN 532 NFC reader, the local database that we use to store play requests (iJukeboxDB), and the main program to run on the jukebox Pi (jukeboxMain.py). (YUNAS FINISH SUMMARY OF ARDUINO FOLDER). 

In the web app folder there is three sub folders, src, server and tests. The src contains all the code to create the frontend GUI (App.js, index.js, login.js, setupproxy.js and all the corresponding css files) and embed a spotify player instance into the web browser (WebPlayback.jsx). The server folder hosts the server that interacts with the spotify API. The tests folder contains tests for ensuring the web app functions properly.

## Installation Instructions & How to Run the System
Start by cloning this repo onto the Jukebox Pi and Speaker Pi, then proceed with the following setup.  

In order to use the project the user is required to create an account with Spotify. Once an account is created the user must register their app with spotify for developers to gain permission to use the API.

### Jukebox Pi
To get the jukebox Pi part of the system operational, attach the PN 532 NFC reader to the GPIO bank on the Pi while the power is disconnected, and plug in the printer cable to the USB port on the Pi and corresponding port on the Arduino. Then open the jukeboxMain.py to make a few edits based on your specific information. First, on line 30 enter your email account you would like notifications to be sent to (right now the notifications only work with Gmail accounts). Next on line 307, change the IP address used in the post request to that of the Speaker Pi you are using. Now you can run this program, and once the other components are started, the iJukebox Pi is ready to rock out!

### Speaker Pi
To run the speaker Pi there are two things you must do to set it up. Firstly in the spotify for developers dahsboard the user must create a callback by editing the app settings. This callback should be for https://'speakerIP':3000/auth/callback. Once that is done all that is left to do is ensure that the .env variables are properly set, the user must input their spotify client ID and secret that they got from registering their app as well as the ip for the PI. Once that is done, simply type "npm run dev" in the web app folder to run the server and GUI.

### Arduinos
(YUNAS EXPLAIN HOW TO SETUP AND RUN ARDUINOS)

## How do you know the system is working properly?
To ensure the sytem is working correctly, you can run the tests found in the end to end communication, and unit test directories and observe their output. If all tests pass then when the main program for the system is run, inserting a card into the display slot and closing the door will start the song playing on the Speaker Pi, the song info will be displayed on the LCD screen, a request log will be seen in both the Firebase and local databases, and you will recieve an email notification with info about what song was played.

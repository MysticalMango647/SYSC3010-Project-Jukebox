#The scope of this is to use selinum to get the ip address of a raspberry pi and open spotify directly on a webpage, that way it is completly automate the process for the end user
#This feature was not integrated, but keeping it here, for future expansions incase

import socket

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def openSpotifyPage():
    link = socket.gethostbyname(socket.gethostname())
    testlink2 = '192.168.0.1'
    port = 3000
    colon = ':'
    httpHeader = 'http://'
    spotifyPage = httpHeader + str(link) + colon + str(port)
    print(spotifyPage)
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get(spotifyPage)

if __name__ == '__main__':
    openSpotifyPage()
    #driver = webdriver.Chrome('./chromedriver')
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.maximize_window()
    #driver.get('http://192.168.0.1')
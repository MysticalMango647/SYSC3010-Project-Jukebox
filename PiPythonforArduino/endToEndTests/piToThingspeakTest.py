# imports
import requests
import time
 
#reading from flynn' channel
readKey = "K48QT1XG8S99VQRM"
channelNumber = "1671152"
url = "https://api.thingspeak.com/channels/" + channelNumber + "/feeds.json"
results = 2
 
def main():
    # payload includes the headers to be sent with the GET request
    # read the documentation for more information (https://docs.python-
    #requests.org)
    payload = {'api_key': readKey, 'results': results}
 
    temp = ""
    
    while True:
        # Sends an HTTP GET request
        response = requests.get(url, params=payload)
        response = response.json()
     
        
         
        entries = response['feeds']
        # Print out the temperature at each entry's time
        e = entries[-1]
        #for e in entries:
        #create message with readings
        data = e['field1']
        if data != temp:
            #print("Channel Name: {}".format(response['channel']['name']))
            print("Data: " + data)
            temp = data
        #print("At {}, the temperature was {}".format(e['created_at'], e['field1']))
        time.sleep(5)
 
if __name__ == "__main__":
    main()


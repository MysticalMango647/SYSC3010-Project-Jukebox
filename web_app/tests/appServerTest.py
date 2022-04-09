#!/usr/bin/env python3
import requests

##Sending valid link

r = requests.post('http://172.17.152.53:5000/play/spotify:album:4wExFfncaUIqSgoxnqa3Eh')

if(r.status_code == 200):
  print('Valid song change Passed')
else:
  print('Valid song change Failed')


r = requests.get('http://172.17.152.53:5000/auth/token')

if(r.text != ''):
  print('Received valid token: ' + r.text)
else:
  print('didnt receive token')

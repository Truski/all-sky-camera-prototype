#### 0. Imports, initiatilizing variables
#########################################

import requests
import base64
import json
from io import BytesIO
from time import sleep,time
from picamera import PiCamera

from astral import Location, Astral

configfile = open('config.json')
cfg = json.load(configfile)

server = cfg['server']
port = cfg['port']
endpoint = cfg['endpoint']
device_name = cfg['name']

camera = PiCamera()

camera.resolution = ''

camera.framerate = 1
camera.awb_mode = 'off'
camera.iso = 800

sleep(30)

camera.exposure_mode = 'off'

l = Location()

l.name = 'current'
l.region = 'region'
l.latitude = cfg['latitude']
l.longitude = cfg['longitude']
l.timezone = 'America/Chicago'
l.elevation = cdf['elevation']
l.sun()




#### 1. Function definitions
#########################################

def take_image(name): 
    camera.capture(name+".jpg")

def translate_image():
    # Takes stream jpeg and converts it to base64



#### 2. Primary while loop
#########################################

while(True):
    file_name = str(device_name) + str(time)
    take_image(file_name)
    # Translate image
    # Send image


uploadURL = f"http://{server}:{port}/{endpoint}"

file = open('images/meteor.jpg', 'rb')

jpeg_text = base64.b64encode(file.read())
data = {
	'time': time(),
	'lat': ,
	'long': -21.311,
	'image': str(jpeg_text)[1:]
}

r = requests.put(uploadURL, json=data)

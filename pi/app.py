#### 0. Imports, initiatilizing variables
#########################################

import requests
import time
import base64
from io import BytesIO
from time import sleep
from picamera import PiCamera

server = 'localhost'
port = '80'
endpoint = 'upload'

#### 1. Function definitions
#########################################

def take_image():
    # Take an image, save it to stream 
    my_stream = BytesIO()
    camera = PiCamera()
    camera.capture(my_stream, 'jpeg')

def translate_image():
    # Takes stream jpeg and converts it to base64



#### 2. Primary while loop
#########################################

while(True):
    # Take image
    # Translate image
    # Send image


uploadURL = f"http://{server}:{port}/{endpoint}"

file = open('images/meteor.jpg', 'rb')

jpeg_text = base64.b64encode(file.read())
data = {
	'time': time.time(),
	'lat': ,
	'long': -21.311,
	'image': str(jpeg_text)[1:]
}

r = requests.put(uploadURL, json=data)

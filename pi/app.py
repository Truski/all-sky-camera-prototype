import requests
import time
import base64

server = 'localhost'
port = '80'
endpoint = 'upload'

uploadURL = f"http://{server}:{port}/{endpoint}"

file = open('images/meteor.jpg', 'rb')

jpeg_text = base64.b64encode(file.read())
data = {
	'time': time.time(),
	'lat': 54.232,
	'long': -21.311,
	'image': str(jpeg_text)[1:]
}

r = requests.put(uploadURL, json=data)
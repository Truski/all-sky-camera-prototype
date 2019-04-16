#### 0. Imports, initiatilizing variables
#########################################

import requests
import base64
import json
import os
from io import BytesIO
from time import sleep,time
from picamera import PiCamera

from astral import Location, Astral

def lcm(x, y, z):
    gcd2 = gcd(y, z)
    gcd3 = gcd(x, gcd2)
    lcm2 = y*z // gcd2
    lcm3 = x*lcm2 // gcd(x, lcm2)

    return lcm3


configfile = open('config.json')
cfg = json.load(configfile)

server = cfg['server']
port = cfg['port']
aws_key = cfg['aws_key']
image_endpoint = cfg['image_endpoint']
raw_endpoint = cfg['raw_endpoint']
status_endpoint = cfg['status_endpoint']
config_endpoint = cfg['config_endpoint']

device_name = cfg['name']

raw_frequency = cfg['raw_frequency']
img_frequency = cfg['img_frequency']
sts_frequency = cfg['sts_frequency']
max_frequency = lcm(raw_frequency, img_frequency, sts_frequency)

image_url = f"http://{server}:{port}/{image_endpoint}"
raw_url = f"http://{server}:{port}/{raw_endpoint}"
status_url = f"http://{server}:{port}/{status_endpoint}"
config_url = f"http://{server}:{port}/{config_enpoint}"

camera = PiCamera()
camera.resolution = ''
camera.framerate = 1
camera.awb_mode = 'off'
camera.iso = 800

sleep(30) # Why?

camera.exposure_mode = 'off'

l = Location()

l.name = 'current'
l.region = 'region'
l.latitude = cfg['latitude']
l.longitude = cfg['longitude']
l.timezone = 'America/Chicago'
l.elevation = cdf['elevation']
l.sun()

record_count = 0

#### 1. Function definitions
#########################################

#### _) Networking

def make_request(url, req_type, data):
    if req_type == "post":
	requests.post(url, json=data, headers="x-api-key": aws_key)
    elif req_type == "get":
	requests.get(url, json=data, headers="x-api-key": aws_key)

#### a) Image Processing

def submit_img_data():
    current_time = str(time())
    file_name = str(device_name) + "-" + current_time + ".jpg"
    take_image(file_name)
    img_data = convert_image_to_base64(file_name)
    send_image(img_data, current_time)
    delete_image(file_name)

def take_image(filename): 
    camera.capture(name)

def convert_image_to_base64(filename):
    file = open(filename, 'rb')
    jpeg_in_base64 = base64.b64encode(file)
    close(file)
    return jpeg_in_base64
    
def send_image(img_data, current_time):
    data = {
	'time': current_time,
	'image': str(img_data)[1:],
	'device': device_name
    }
    print(data)
    make_request(image_url, 
    r = requests.put(image_url, json=data)
    
def delete_image(filename):
    os.remove(filename)

#### b) Raw Data Processing

def submit_raw_data():
    data = capture_raw_data()
    send_raw(data)

def capture_raw_data():
    # TODO: Yogi and Koushik

def send_raw(data):
    requests.put(raw_url, data)

#### c) Status Upload

def submit_status():
    # TODO: Aziz

#### 2. Primary while loop
#########################################

while(True):
    sleep(1)
    
    print("Time is" + str(record_count)
    
    if record_count % raw_frequency == 0:
	print("Submitting raw data")
	submit_raw_data()
	
    if record_count % img_frequency == 0:
	print("Submitting img data")
	#submit_img_data()
    
    if record_count % sts_frequency == 0:
	print("Submitting status")
	submit_status()
	
    record_count += 1
    
    if record_count == max_frequency:
	record_count = 0

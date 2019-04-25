#### 0. Imports, initiatilizing variables
#########################################

from time import sleep,time
import sys

print("Brolo")
sys.stdout.flush()

sleep(120)

import requests
import base64
import json
import os
from math import gcd
from picamera import PiCamera
from astral import Location, Astral
import serial

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
api_key = cfg['api_key']
image_endpoint = cfg['image_endpoint']
raw_endpoint = cfg['raw_endpoint']
status_endpoint = cfg['status_endpoint']
config_endpoint = cfg['config_endpoint']

device_name = cfg['device_name']

raw_frequency = cfg['raw_frequency']
img_frequency = cfg['img_frequency']
sts_frequency = cfg['sts_frequency']
max_frequency = lcm(raw_frequency, img_frequency, sts_frequency)

image_url = f"{server}:{port}/{image_endpoint}"
raw_url = f"{server}:{port}/{raw_endpoint}"
status_url = f"{server}:{port}/{status_endpoint}"
config_url = f"{server}:{port}/{config_endpoint}"

print("Image url: " + image_url)
print("Api key: " + api_key)

camera = PiCamera()
camera.resolution = '2592x1944'
camera.framerate = 1
#camera.awb_mode = 'off'
camera.iso = 800

# ser = serial.Serial("/dev/ttyACM0",9600)

camera.exposure_mode = 'off'

l = Location()

l.name = 'current'
l.region = 'region'
l.latitude = cfg['latitude']
l.longitude = cfg['longitude']
l.timezone = 'America/Chicago'
l.elevation = cfg['elevation']
l.sun()

record_count = 0

#### 1. Function definitions
#########################################

#### _) Networking

def make_request(url, req_type, data):
    r = ""
    if req_type == "post":
        r = requests.post(url, json=data, headers={"x-api-key": api_key, "content-type": "application/json"})
    elif req_type == "get":
        r = requests.get(url, json=data, headers={"x-api-key": api_key, "content-type": "application/json"})
    print(r)
    print(r.text)

#### a) Image Processing

def submit_img_data():
    current_time = str(time())
    file_name = str(device_name) + "-" + current_time + ".jpg"
    take_image(file_name)
    img_data = convert_image_to_base64(file_name)
    send_image(img_data, current_time)
    delete_image(file_name)

def take_image(filename): 
    camera.capture(filename)

def convert_image_to_base64(filename):
    file = open(filename, 'rb')
    jpeg_in_base64 = base64.b64encode(file.read())
    file.close()
    return jpeg_in_base64
    
def send_image(img_data, current_time):
    data = { 'time': current_time, 'img': str(img_data)[1:] }
    make_request(image_url, "post", data)

def delete_image(filename):
    os.remove(filename)

#### b) Raw Data Processing

def submit_raw_data():
    data = {
	'raw_data': capture_raw_data()	
    }
    send_raw(data)

def capture_raw_data():
    #ser.flush()
    #return ser.readline()
    return "this is some data dude"

def send_raw(data):
    make_request(raw_url, "post", data)

#### 2. Primary while loop
#########################################

while True:
    sleep(1)
    if record_count % raw_frequency == 0:
        print("Submitting raw data")
        submit_raw_data()
	
    if record_count % img_frequency == 0:
        print("Submitting img data")
        submit_img_data()
    
    if record_count % sts_frequency == 0:
        print("Submitting status")
	
    record_count += 1
    
    if record_count == max_frequency:
        record_count = 0

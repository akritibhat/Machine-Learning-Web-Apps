import requests
from flask import Flask,render_template,request,url_for

import time

#EDA Packages
import pandas as pd
import numpy as np

# ML Packages

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import psycopg2

from libsoundtouch import soundtouch_device
from libsoundtouch.utils import Source, Type

import pprint
import sys

import spotipy
import spotipy.util as util

app = Flask(__name__)


@app.route("/")
def index():
	#startDj()
	#connectToDB()
	#send_sms('+18572648772')
	return render_template("index.html")


def connectToDB():
	con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="34.67.145.3", port="5432")

	print("Database opened successfully")

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()


    # Add a message
    resp.message("Thank you for your bid!")
    return str(resp)

def send_sms(number):
	print(number)
	account_sid = 'ACf3d029ace0ab2f696f9f971c11696f91'
	auth_token = '14ac526739b259838c2f67becc772b6f'
	client = Client(account_sid, auth_token)

	message = client.messages \
		.create(
		body="Your Bidding Won",
		from_='+12028312095',
		to=number
	)

	print(message.sid)


def playSong(track):
	print("i am playing song")
	url = "http://192.168.1.168:8090/speaker"

	payload = "<play_info><app_key>L8QYEJtiHzmtZ6EJg8ETr9WB8HbCdYkl</app_key><url>"+track+"</url><service>service text</service><reason>reason text</reason><message>message text</message><volume>50</volume></play_info>"
	headers = {
		'Content-Type': "text/plain",
		'User-Agent': "PostmanRuntime/7.15.0",
		'Accept': "*/*",
		'Cache-Control': "no-cache",
		'Postman-Token': "f9cd60fb-a7f2-45b4-9398-c5ece6112d1d,abb8f174-a27f-410e-9677-22950e096b83",
		'Host': "192.168.1.168:8090",
		'accept-encoding': "gzip, deflate",
		'content-length': "261",
		'Connection': "keep-alive",
		'cache-control': "no-cache"
	}

	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.text)


def playSong1(track):
	device = soundtouch_device('192.168.1.168')
	print(device.status().content_item.source_account)
	#device.power_on()
	trackToPlay = 'spotify:track:'+track
	print(device.config.name)
	resp = device.play_media(Source.SPOTIFY, trackToPlay, '5yz9rfw854rb39vkepel9jh3f')
	print(resp)


def getCurrentSongDuration():
	URL = "http://192.168.1.168:8090/now_playing"
	device = soundtouch_device('192.168.1.168')
	print(device.status().content_item.source_account)
	# device.power_on()
	print(device.config.name)
	resp = (device.status())

	return resp.duration


def startDj():

	i = 0
	track = getNextSong()
	playSong1(track)

	while i < 6 :
		track = getNextSong()
		playSong1(track)
		timeToSleep = getCurrentSongDuration()
		time.sleep(timeToSleep)
		i = i+1



def getNextSong():
	return "0tBbt8CrmxbjRP0pueQkyU"

@app.route("/pauseSong", methods=['GET', 'POST'])
def pauseSong():
	url = "http://192.168.1.168:8090/key"

	payload = "<key state=\"press\" sender=\"Gabbo\">PLAY_PAUSE</key>"
	headers = {
		'Content-Type': "text/plain",
		'User-Agent': "PostmanRuntime/7.15.0",
		'Accept': "*/*",
		'Cache-Control': "no-cache",
		'Postman-Token': "5d036cf0-9330-42ef-8197-a224cfc4036a,12a332e9-be32-440d-9cf5-dce748f6b16e",
		'Host': "192.168.1.168:8090",
		'accept-encoding': "gzip, deflate",
		'content-length': "50",
		'Connection': "keep-alive",
		'cache-control': "no-cache"
	}

	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.text)




if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)
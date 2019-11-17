import requests
from flask import Flask,render_template,request,url_for
import json
import time
import mysql.connector

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from libsoundtouch import soundtouch_device
from libsoundtouch.utils import Source, Type

app = Flask(__name__)

songBeingPlayed = 0
songPlayedName = "test"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
	mobile_no = request.values.get('From',None)
	body = request.values.get('Body', None)
	songId = body.split(" ")[0]
	bidAmt = body.split(" ")[1]
	res = update(mobile_no,bidAmt,songId)
	resp = MessagingResponse()
	if res :
		send_sms(mobile_no,"Thank you for your bid!")
	else :
		send_sms(mobile_no,"Not Enough Credit!")


def send_sms(number, messageBody):
	print(number)
	account_sid = 'ACf3d029ace0ab2f696f9f971c11696f91'
	auth_token = '14ac526739b259838c2f67becc772b6f'
	client = Client(account_sid, auth_token)

	message = client.messages \
		.create(
		body=messageBody,
		from_='+12028312095',
		to=number
	)
	print(message.sid)


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
	while i < 6 :
		track = getNextSong()
		playSong1(track)
		print(currentBid())
		timeToSleep = getCurrentSongDuration()
		time.sleep(timeToSleep)
		i = i+1



def getNextSong():
	cnx = mysql.connector.connect(user='be3bc40df921df', password='c7708685',
								  host='us-cdbr-iron-east-04.cleardb.net',
								  database='heroku_67d188873be555e')

	cursor = cnx.cursor()
	query = ("select id, song_name, song_id from songs order by bid_amt desc limit 1;")
	cursor.execute(query)

	for  (id) in cursor:
		id_temp =  id[2]
		songPlayedName = id[1]
		songBeingPlayed = id_temp
		id_song = id[0]

	BASE_URL = 'delete from songs where id = '

	query2 = (BASE_URL +  str(id_song) +';')
	cursor.execute(query2)
	cnx.commit()
	cursor.close()
	cnx.close()
	return id_temp

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


@app.route("/current", methods=['GET', 'POST'])
def currentSong():
	return songPlayedName


@app.route("/bidData", methods=['GET', 'POST'])
def currentBid():
	cnx = mysql.connector.connect(user='be3bc40df921df', password='c7708685',
								  host='us-cdbr-iron-east-04.cleardb.net',
								  database='heroku_67d188873be555e')

	cursor = cnx.cursor()
	query = ("select song_name, bid_amt from songs order by bid_amt desc;")
	cursor.execute(query)

	songs = []
	bids = []
	for (id) in cursor:
		songs.append(id[0])
		bids.append(id[1])

	song_json = []
	for i in range(len(bids)):
		song_json.append({'name': songs[i], 'bid': bids[i]})


	cursor.close()
	cnx.close()
	return json.dumps(song_json)


def update(phoneNum, bid, song_id):
	ph = phoneNum
	ph = ph.replace("+","")
	cnx = mysql.connector.connect(user='be3bc40df921df', password='c7708685',
								  host='us-cdbr-iron-east-04.cleardb.net',
								  database='heroku_67d188873be555e')

	cursor = cnx.cursor()
	query = ("select id, credits from users where mob_num=" + str(ph) + ";")
	cursor.execute(query)

	for (id) in cursor:
		user_id = id[0]
		user_bid = id[1]
		if bid > id[0]:
			return False

	query4 = ("select bid_amt from songs where id=" + str(song_id) + ";")
	cursor.execute(query4)

	for (id) in cursor:
		song_bid = id[0]

	query2 = ("update users set credits = " + str(user_bid - bid) + " where id = " + str(user_id) + ";")
	cursor.execute(query2)
	query3 = ("update songs set bid_amt = " + str(song_bid + bid) + " where id =" + str(song_id) + ";")
	cursor.execute(query3)

	cnx.commit()
	cursor.close()
	cnx.close()
	return True


if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)
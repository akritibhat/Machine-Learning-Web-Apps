from flask import Flask,render_template,request,url_for
import pandas as pd
import numpy as np
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import psycopg2
import json
import pprint
import sys
import spotipy
import spotipy.util as util

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
	# connectToDB()
	#send_sms('+18572648772',"Your Bidding Won")
	return render_template("main.html")

def placeBid(id, bid):
	con.execute('select credits from users where id={};'.format(bid))
	credits = con.fetchone()
	if credits >= bid:
		con.execute('update users set credits={} where id={};'.format(credits-bid,id))
	else:
		con.execute('select phone_number from users where id={};'.format(id))
		send_sms(con.fetchone(), "You don't have enough credits. Credits:{}".format(credits))

def getNextSong():
	con.execute('select id from songs order by bid_amount desc limit 1;')
	nSong_id=con.fetchone()
	con.execute('update songs set cur_song='t' where id={}'.format(nSong_id))
	return nSong_id

def deleteSong(id):
	con.execute('delete from songs where id={};'.format(id))


def getJSON():
	con.execute('select sum(cur_big) from songs;')
	totalRaised = con.fetchone()
	con.execute('select song_name from songs where cur_song='t';)
	current = con.fetchone()
	con.execute('select song_name, cur_bid from songs order by cur_bid desc limit 6;')
	vals = con.fetchall()
	while len(vals) < 6:
		vals.append("N/A", 0)

	return {
	"totalRaised": [{
		"cur_bid": %d
	}],
	"current": [{
		"song_name": %s
	}],
	"nextOne": [{
		"song_name": %s,
		"cur_bid": %d
	}],
	"nextTwo": [{
		"song_name": %s,
		"cur_bid": %d
	}],
	"nextThree": [{
		"song_name": %s,
		"cur_bid": %d
	}],
	"nextFour": [{
		"song_name": %s,
		"cur_bid": %d
	}],
	"nextFive": [{
		"song_name": %s,
		"cur_bid": %d
	}]
}" % (totalRaised, current, vals[0][0], 
	vals[0][1],vals[1][0], vals[1][1],
	vals[2][0], vals[2][1],vals[3][0],
	vals[3][1],vals[4][0], vals[4][1],
	vals[5][0], vals[5][1],)

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

def send_sms(number, msg):
	print(number)
	account_sid = 'ACf3d029ace0ab2f696f9f971c11696f91'
	auth_token = '14ac526739b259838c2f67becc772b6f'
	client = Client(account_sid, auth_token)

	message = client.messages \
		.create(
		body=msg,
		from_='+12028312095',
		to=number
	)

	print(message.sid)

if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)

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

app = Flask(__name__)

@app.route("/")
def index():
	connectToDB()
	#send_sms('+18572648772')
	return render_template("index.html")

def placeBid(id, bid):
	con.execute('select credits from users where id={};'.format(bid))
	credits = con.fetchone()
	if credits >= bid:
		con.execute('update users set credits={} where id={};'.format(credits-bid,id))
	else:
		con.execute('select phone_number from users where id={};'.format(id))
		send_sms(con.fetchone(), "You don't have enough credits. Credits:{}".format(credits))

def getNextSong():
	song_id = int(con.execute('select id from songs order by bid_amount desc limit 1;'))
	con.execute('delete from songs where id={};'.format(id))

def getJSON():
	x=[con.execute('select sum(cur_bid) from songs;'),
	con.execute('select song_name from songs where cur_song = 't';'),
	con.execute('select song_name from songs where cur_song = 't';'),
	con.execute('select cur_bid from songs where cur_song = 't';'),

	 ]
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
}" % ()

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

@app.route("/",methods=['POST'])
def predict():
	# Link to dataset from github
	url = "https://raw.githubusercontent.com/Jcharis/Machine-Learning-Web-Apps/master/Youtube-Spam-Detector-ML-Flask-App/YoutubeSpamMergedData.csv"
	df= pd.read_csv(url)
	df_data = df[["CONTENT","CLASS"]]
	# Features and Labels
	df_x = df_data['CONTENT']
	df_y = df_data.CLASS
    # Extract Feature With CountVectorizer
	corpus = df_x
	cv = CountVectorizer()
	X = cv.fit_transform(corpus) # Fit the Data
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.33, random_state=42)
	#Naive Bayes Classifier
	from sklearn.naive_bayes import MultinomialNB
	clf = MultinomialNB()
	clf.fit(X_train,y_train)
	clf.score(X_test,y_test)
	#Alternative Usage of Saved Model
	# ytb_model = open("naivebayes_spam_model.pkl","rb")
	# clf = joblib.load(ytb_model)

	if request.method == 'POST':
		comment = request.form['comment']
		data = [comment]
		vect = cv.transform(data).toarray()
		my_prediction = clf.predict(vect)
	return render_template('results.html',prediction = my_prediction,comment = comment)



if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)

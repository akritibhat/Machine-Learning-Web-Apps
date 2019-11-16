from flask import Flask,render_template,request,url_for

#EDA Packages
import pandas as pd
import numpy as np
import psycopg2

db_user = "postgres"
db_password = "postgres"
db_name = "postgres"
db_connection_name = "bostonhacks-259202:us-central1:bh-data"

# ML Packages
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
app = Flask(__name__)

@app.route("/")
def index():
	# When deployed to App Engine, the `GAE_ENV` environment variable will be
	# set to `standard`
	if os.environ.get('GAE_ENV') == 'standard':
	# If deployed, use the local socket interface for accessing Cloud SQL
		host = '/cloudsql/{}'.format(db_connection_name)
	else:
	# If running locally, use the TCP connections instead
	# Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
	# so that your application can use 127.0.0.1:3306 to connect to your
	# Cloud SQL instance
		host = '127.0.0.1'

	cnx = psycopg2.connect(dbname=db_name, user=db_user,
	                   password=db_password, host=host)
	with cnx.cursor() as cursor:
		cursor.execute('SELECT * from users;')
		result = cursor.fetchall()
	current_time = result[0][0]
	cnx.commit()
	cnx.close()

	return (result)

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

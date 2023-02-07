# Test microblog project on Flask.

import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
	app = Flask(__name__)
	client = MongoClient(os.getenv('MONGODB_URI'))
	app.db = client.microblog

	@app.route('/', methods=['GET', 'POST'])
	def home():
		if request.method == 'POST':
			entry_content = request.form.get('content')
			if len(entry_content) > 0:
				formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
				app.db.entries.insert_one({'content': entry_content, 'date': formatted_date})
		entries_with_date = []
		for entry in app.db.entries.find({}):
			entries_with_date.append((
				entry['content'], 
				entry['date'],
				datetime.datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d'),
			))
		return render_template('home.html', entries=entries_with_date)

	return app
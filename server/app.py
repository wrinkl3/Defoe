#!flask/bin/python
from flask import Flask, jsonify, current_app, abort, request
from django.core.validators import URLValidator
from django.conf import settings
import urllib
from screenshooter import Screenshooter
from classifier import DefacementClassifier

app = Flask(__name__, static_url_path='')
shooter = Screenshooter()
defacementClassifier = DefacementClassifier()
settings.configure(DEBUG=False)
validator = URLValidator()

def decode(url):
	return urllib.unquote(url).decode('utf8')

@app.route('/defoe/api/v1.0/<string:page_url>', methods=['GET'])
def check_defacement(page_url):
	try:
		assert len(page_url)>8
		url = decode(page_url)
		validator(url)
		screenshot_path = shooter.screenshot(url)
		label = defacementClassifier.isDefaced(screenshot_path)
		label = 'true' if label else 'false'
	except Exception as inst:
		print inst
		return abort(400)
	else:
		return jsonify({'isDefaced': label})


@app.route('/defoe/api/v1.0/report', methods=['POST'])
def report_defacement():
	try:
		assert request.json and 'url' in request.json and 'isDefaced' in request.json
		page_url = request.json['url']
		isDefaced = request.json['isDefaced']
		url = decode(decode(page_url))
		validator(url)
		screenshot_path = shooter.screenshot(url)
		defacementClassifier.train(screenshot_path, isDefaced)
		return '', 201
	except Exception as inst:
		print request.json
		return abort(400)




@app.route('/')
def root():
	return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
import json
import time
import subprocess
import urllib
import urllib2
import RPi.GPIO as GPIO
from flask import Flask, request

app = Flask(__name__)
ledPin = 21

@app.route("/light")
def light():
	global ledOn
	GPIO.output(ledPin, ledOn)
	ledOn = not ledOn
	return 'light on'

@app.route("/deploy", methods=['POST'])
def deploy():
	data = json.loads(request.get_data())
	user_agent="Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5." 
	tl = 'fr'
	url = 'http://translate.google.com/translate_tts'
	words = data['message'].split()
	for word in words:
		params = urllib.urlencode({'q':word, 'tl':tl})
		req = urllib2.Request(url, params)
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req) 
		with open(word, 'wb') as file:
            		file.write(response.read())

	for word in words:
		subprocess.call(['omxplayer', '-o', 'local', word])
		time.sleep(0.5)
	return 'hello'

if __name__ == "__main__":
	ledOn = True
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ledPin, GPIO.OUT)
	app.run('0.0.0.0', debug=True, port=12346)

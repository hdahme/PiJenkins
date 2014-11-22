import json
import time
import subprocess
import urllib
import urllib2
import unirest
import RPi.GPIO as GPIO
from flask import Flask, request

app = Flask(__name__)
ledPin = 21

@app.route("/light")
def light():
    GPIO.output(ledPin, True)
    return 'light on'
    
def chunk_words(phrase):
    return [phrase]

@app.route("/deploy", methods=['POST'])
def deploy():
    # For documentation, etc
    # https://www.mashape.com/voicerss/text-to-speech-1
    # http://www.voicerss.org/api/documentation.aspx
    data = json.loads(request.get_data())
    phrase = data['message'].replace(' ', '%2C+')
    audio_file = 'temp.mp3'
    response = unirest.get("https://voicerss-text-to-speech.p.mashape.com/?key=a53b7934b4354456b9cceef9318c0e5c&c=mp3&f=22khz_8bit_mono&hl=en-gb&r=0&src={0}".format(phrase),
        headers={
            "X-Mashape-Key": "kJAXv7SL9QmshLDuufl6MfoVFeJyp10JEWOjsnn0fOpug9eEXU"
        }
    )

    with open(audio_file, 'wb') as file:
        file.write(response.raw_body)

    subprocess.call(['omxplayer', '-o', 'local', audio_file])
    return data['message']

if __name__ == "__main__":
    ledOn = True
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin, GPIO.OUT)
    app.run('0.0.0.0', debug=True, port=12346)
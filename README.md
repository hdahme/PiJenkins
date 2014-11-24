PiJenkins
=========

A text to speech flask app, meant to be run on a Pi hooked up to a speaker

Setup
-----
Give your pi a static ip and plug it in to a speaker/headphones
Run the flask app from your pi
```
sudo python server.py
```

Usage
-----
CURL your Pi's IP, port 12346 with a post payload of {'message': 'Hello world'}. Eg
```
curl pi:12346/deploy -XPOST -d '{"message":"yolo swag"}'
```

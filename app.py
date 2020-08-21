#!./venv/bin/python python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session
from glob import glob

# https://pypi.org/project/Flask-JWT/
# https://pypi.org/project/Flask-SocketIO/
# https://github.com/nanomosfet/WebRTC-Flask-server/tree/master/webRTCserver

app = Flask(__name__)
app.secret_key = b'isthisgoodenought?'
app.SESSION_COOKIE_SECURE = True

@app.route('/')
def index():
    dm_images = []
    for img in glob('static/DM_Maps/*'):
        dm_images.append(img)
    player_images = []
    for img in glob('static/Player_Maps/*'):
        player_images.append(img)

    return render_template('index.html', player_images=player_images, dm_images=dm_images)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

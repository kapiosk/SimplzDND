#!./venv/bin/python python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session
from glob import glob
from flask_socketio import SocketIO
import datetime

# https://github.com/nanomosfet/WebRTC-Flask-server/tree/master/webRTCserver

app = Flask(__name__)
app.secret_key = b'isthisgoodenought?'
app.SESSION_COOKIE_SECURE = True
sio = SocketIO(app)

connected_particpants = {}

@app.route('/')
def index():
    dm_images = []
    for img in glob('static/DM_Maps/*'):
        dm_images.append(img)
    player_images = []
    for img in glob('static/Player_Maps/*'):
        player_images.append(img)

    return render_template('index.html', player_images=player_images, dm_images=dm_images)


def write_log(s):
    with open('logfile.out', 'a+') as f:
        f.write('time: %s Action: %s \n' % (str(datetime.datetime.now()), s))


@sio.on('message', namespace='/')
def messgage(sid, data):
    sio.emit('message', data=data)


@sio.on('disconnect', namespace='/')
def disconnect(sid):
    write_log("Received Disconnect message from %s" % sid)
    for room, clients in connected_particpants.iteritems():
        try:
            clients.remove(sid)
            write_log("Removed %s from %s \n list of left participants is %s" % (
                sid, room, clients))
        except ValueError:
            write_log("Remove %s from %s \n list of left participants is %s has failed" % (
                sid, room, clients))


@sio.on('create or join', namespace='/')
def create_or_join(sid, data):
    sio.enter_room(sid, data)
    try:
        connected_particpants[data].append(sid)
    except KeyError:
        connected_particpants[data] = [sid]
    numClients = len(connected_particpants[data])
    if numClients == 1:
        sio.emit('created', data)
    elif numClients > 2:
        sio.emit('full')
    elif numClients == 2:
        sio.emit('joined')
        sio.emit('join')
    print(sid, data, len(connected_particpants[data]))


@app.route('/room/<room>')
def room(room):
    return render_template('room.html', room=room)

if __name__ == '__main__':
    if True:
        sio.run(app, host='0.0.0.0', port=5000)
    else:
        sio.run(app, host='0.0.0.0', port=5000, ssl_context='adhoc')

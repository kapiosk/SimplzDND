from flask import Flask, redirect, render_template, request, session, url_for
from os import path

app = Flask(__name__)
app.secret_key = b'isthisgoodenought?'
app.SESSION_COOKIE_SECURE = True

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
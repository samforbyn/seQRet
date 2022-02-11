from smtpd import DebuggingServer
from flask import Flask, render_template, redirect, request
from models import create_post

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")
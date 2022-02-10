from flask import Flask, render_template, redirect, request

app = Flask(__name__)

app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "GET":
        pass

    if request.method == "POST":
        name = request.form.get("name")
        post = request.form.get("post")        
        create_post(name, post)

    return render_template('index.html')


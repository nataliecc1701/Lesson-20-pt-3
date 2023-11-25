from flask import Flask, request, render_template
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)
app.config["SECRET_KEY"] = "shhhh!!"
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def index_route():
    return render_template("satisfaction.html")
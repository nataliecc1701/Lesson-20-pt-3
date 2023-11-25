from flask import Flask, request, render_template, redirect, flash
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)
app.config["SECRET_KEY"] = "shhhh!!"
debug = DebugToolbarExtension(app)

responses = []
current_survey = satisfaction_survey

@app.route("/")
def index_route():
    return render_template("instructions.html", survey = current_survey)

@app.route("/questions/<question_num>")
def question_route(question_num):
    return render_template("question.html",
                           question_num = int(question_num), survey = current_survey,
                           question=current_survey.questions[int(question_num)])

@app.route("/answer", methods=["POST"])
def record_answer():
    ans = request.form.get("survey-question", None)
    if ans:
        responses.append(ans)
    else:
        flash("Answer Required!")
    # this should send you to the right page regardless
    # (unless it sends you out of bounds or you've been manually inputting question numbers)
    return redirect("/questions/" + str(len(responses)))
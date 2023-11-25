from flask import Flask, request, render_template, redirect, flash, session
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)
app.config["SECRET_KEY"] = "shhhh!!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

current_survey = satisfaction_survey

@app.route("/")
def index_route():
    return render_template("instructions.html", survey = current_survey)

@app.route("/new", methods=["POST"])
def start_new_session():
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<question_num>")
def question_route(question_num):
    if int(question_num) == len(session["responses"]):
        return render_template("question.html",
                           question_num = int(question_num), survey = current_survey,
                           question=current_survey.questions[int(question_num)])
    else:
        if len(session["responses"]) < len(current_survey.questions):
            flash("Questions must be done in order!")
            return redirect("/questions/" + str(len(session["responses"])))
        else:
            flash("The survey has already been completed")
            return redirect("/thank-you")

@app.route("/answer", methods=["POST"])
def record_answer():
    ans = request.form.get("survey-question", None)
    
    if len(session["responses"]) > int(request.referrer[-1]):
        flash ("Question already answered!")
    elif ans:
        rsps = session["responses"]
        rsps.append(ans)
        session["responses"] = rsps
    else:
        flash("Answer Required!")
    
    if len(session["responses"]) < len(current_survey.questions):
        return redirect("/questions/" + str(len(session["responses"])))
        # this should go to the next page if you answered or back to the current one
        # if you did not
    else:
        return redirect("/thank-you")
    
@app.route("/thank-you")
def thank_you():
    return render_template("thank-you.html", survey=current_survey, responses=session["responses"])
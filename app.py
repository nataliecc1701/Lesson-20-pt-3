from flask import Flask, request, render_template
from surveys import *

app=Flask(__name__)

responses = []


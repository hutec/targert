import os
import sys

from flask import Flask, render_template
from flask.ext.bower import Bower

app = Flask(__name__)
app.config.from_object('config')
from app import views

Bower(app)


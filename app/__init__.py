import os
import sys

from flask import Flask, render_template
from flask.ext.bower import Bower
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy

from api_resources import IgnoreItem

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

api = Api(app) 
api.add_resource(IgnoreItem, '/remove/<string:item_id>')

Bower(app)
from app import views



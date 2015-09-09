import os
import sys

from flask import Flask, render_template
from flask.ext.bower import Bower
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
Bower(app)

from ebay import EbayHandler
ebay_handler = EbayHandler()

from api_resources import IgnoreItem, RemoveSearch
api = Api(app) 
api.add_resource(IgnoreItem, '/target/ignore/<string:item_id>')
api.add_resource(RemoveSearch, '/target/remove/<string:title>')

from app import views

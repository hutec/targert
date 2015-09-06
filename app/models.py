from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app import db

class EbayRequest(db.Model):
    __tablename__ = 'searches'
    title = db.Column("title", db.Text, primary_key=True)
    keywords = db.Column("keywords", db.Text)

    def __init__(self, title, keywords):
        self.title = title
        self.keywords = keywords

    def __repr__(self):
        return str(self.title) + " with keywords: " + str(self.keywords)


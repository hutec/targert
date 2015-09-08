import os
import json
from flask import Blueprint, request, render_template, flash, g, session,\
    url_for
from ebay import EbayHandler
from app import app, db
from forms import AddSearchForm
from pprint import pprint
from models import EbayRequest
import urllib

ebay_handler = EbayHandler()


def add_search(title, keywords):
    search = AddSearchForm(title, keywords)
    db.session.add(search)
    db.session.commit()
    # search = {title: {"request": {
    #                     "keywords": keywords,
    #                     "itemFilter": [
    #                         {"name": "LocatedIn", "value": "DE"}
    #                     ]
    #                 }}}
    # path = os.path.dirname(os.path.realpath(__file__)) + "/search.json"
    # json.dump(search, open(path, "a"), indent=4)
         


@app.route('/')
def index():
    return 'Hello world'


@app.route('/target/<title>', methods=['GET'])
@app.route('/target', methods=['GET', 'POST'])
def show_target_page(title=None):
    form = AddSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        search = EbayRequest(title = form.title.data,
                               keywords = form.keywords.data)
        db.session.add(search)
        db.session.commit()
        print("added search " + form.title.data)
        ebay_handler.add_search(search)
        
        #refresh search results

    if title is not None:
        title = urllib.unquote_plus(title)

    return render_template('index.html',
                           #results=ebay_handler.get_cached_results(),
                           results=ebay_handler.get_search_results(title),
                           searches=ebay_handler.get_searches(),
                           #searches=['APC', 'Viberg', 'Red Wing'],
                           form=form)


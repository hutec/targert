from flask import Blueprint, request, render_template, flash, g, session,\
    url_for
from ebay import EbayHandler
from app import app
from pprint import pprint

ebay_handler = EbayHandler()

@app.route('/')
def index():
    return 'Hello world'


@app.route('/target')
def show_target_page():
    results = []
    for req in ebay_handler.search_requests:
        results.extend(ebay_handler.get_multi_page_result(req, 2))
    return render_template('index.html', results=results)


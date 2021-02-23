#!/usr/bin/env python

# https://kb.objectrocket.com/elasticsearch/how-to-setup-a-mongodb-app-using-the-flask-framework-557
# https://pythonbasics.org/flask-mongodb/
# https://kanchanardj.medium.com/how-to-display-database-content-in-your-flask-website-8a62492ba892
# https://stackoverflow.com/questions/57637088/display-mongodb-documents-data-on-a-webpage-using-python-flask
# https://stackoverflow.com/questions/23327293/flask-raises-templatenotfound-error-even-though-template-file-exists
# https://stackoverflow.com/questions/64337951/trouble-charting-with-chartjs-with-data-from-mongodb-using-flask-and-jquery

from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import Flask, render_template, request
from bson.json_util import dumps




app = Flask(__name__)

# export FLASK_APP=hello.py
# flask run --host=0.0.0.0

# connect to mongodb
client = MongoClient()
# default host/port
wsb_db = client["wsbtrends"]
wsb_collection = wsb_db["tickers"]




@app.route('/')
# displays all data in wsb_collection
def findResults():
    try:
        collections_find = wsb_collection.find()
        return render_template('results.html',tasks=collections_find)
    except Exception as e:
        return dumps({'error': str(e)})

if __name__ == '__main__':  
   app.run(debug = True)

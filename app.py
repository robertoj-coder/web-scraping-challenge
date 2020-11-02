import os
from flask import Flask, render_template, redirect, request, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd
from splinter.exceptions import ElementDoesNotExist
app = Flask(__name__)


# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

mars_data = mongo.db.mars_data
# mars_data.drop()

@app.route("/")
def index():
    
    mars_results = list(mars_data.find())
    print(mars_results)
    return render_template("index.html", mars_results=mars_results)
    

@app.route("/scrape")
def scraper():
    
    data = scrape_mars.scrape()
    mongo.db.mars_data.insert_one(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

# Mars_dict = mongo.db.Mars_dict
# Mars_dict.drop()
# # mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# @app.route("/")
# def index():

#     # print("scrape works")
#     # Find one record of data from the mongo database
#     mars_results = list(Mars_dict.find())
#     # Mars_results=mongo.db.Mars_dict.find_one()
#     # mars_results = mongo.db.collection.find_one()

#     # Return template and data
#     return render_template("index.html", mars_results = mars_results)

# @app.route("/scrape")
# def scrape():

#     # print("scrape works")
#     # Mars_data = mongo.db.mars_dict
#     mars_data = scrape_mars.scrape()

#     # print(data)

#     # mongo.db.Mars_data.insert_one(data)
#     # Mars_data.collection.insertOne(mars_info)
#     # Update the Mongo database using update and upsert=True
#     # mongo.db.collection.update({}, mars_data, upsert = True)
#     Mars_dict.update({}, mars_data, upsert=True)
#     return redirect("/")
#     # return "scrapesucceded"

# if __name__ == "__main__":
#     app.run(debug=True)
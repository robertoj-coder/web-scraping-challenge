
from flask import Flask, render_template, redirect, request, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

Mars_dict = mongo.db.Mars_dict

@app.route("/")
def index():

    # Find one record of data from the mongo database
    Mars_results = Mars_dict.find.one()

    # Return template and data
    return render_template("index.html", Mars_results =Mars_results)

@app.route("/scrape")
def scrape():

    mars_dict = mongo.db.mars_dict
    mars_info = scrape_mars.scrape()

    Mars_dict.inser_one(mars_info)
    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_info, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
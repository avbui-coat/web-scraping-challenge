from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scraping

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


# @app.route("/feature_img")
# def image():
#     mars = mongo.db.mars.find_one()
#     return render_template("feature_img.html", mars=mars)

@app.route("/hemisphere")
def news():
    mars = mongo.db.mars.find_one()
    return render_template("hemisphere.html", mars=mars)


@app.route("/facts")
def facts():
    mars = mongo.db.mars.find_one()
    return render_template("mars_facts.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = mars_scraping.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug = True)
from flask import Flask, render_template
from flask_pymongo import PyMongo
import mars_scraping

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# @app.route("/mars_image")
# def image():
#     mars = mongo.db.mars.find_one()
#     return render_template("index.html", mars=mars)

# @app.route("/news")
# def news():
#     mars = mongo.db.mars.find_one()
#     return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = mars_scraping.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug = True)
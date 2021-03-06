from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
# import scrape_craigslist

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    # get the collection
    listings = mongo.db.listings.find_one()
    # call index file in template 
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    #obtain the collection from mongo db
    listings = mongo.db.listings

    # retrieve data from function in scrape_mars lib file
    marsDataDict = scrape_mars.scrape()
    # update new collection
    listings.update({}, marsDataDict, upsert=True)
    #redirect to default page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

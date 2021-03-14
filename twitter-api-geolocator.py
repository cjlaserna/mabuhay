# no language processsomg

from TwitterAPI import TwitterAPI
import geopandas as gpd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from flask import Flask
from flask import render_template

import os
import json

#m

#keys setup
load_dotenv()

consumer_key=os.getenv("CONSUMER_KEY")
consumer_secret=os.getenv("CONSUMER_SECRET")
access_token_key=os.getenv("ACCESS_TOKEN_KEY")
access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")

api = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret)
#end 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    response =api.request("statuses/filter", { "track":["baha", "kailangan"], "locations":[115, 5, 130, 20 ] })

    coordinates = []

    tweets = response.get_iterator()

    count = 0
    while count < 75:
        tweet = next(tweets)
        if "place" in tweet and tweet["place"] != None:
            x, y = tweet["place"]['bounding_box']["coordinates"][0][0]
            if (x >= 115 and x <= 130 and y >= 5 and y <= 20):
                place = tweet["place"]['bounding_box']["coordinates"][0][0]
                coordinates.append(place)
                count += 1

    ph_map = gpd.read_file("shapefiles\gadm36_PHL_1.shp")

    fig, ax = plt.subplots(figsize = (15,15))
    ph_map.plot(ax=ax)

    for x, y in coordinates:
        plt.scatter(x, y, marker="o", color="red")

    plt.savefig("static/map.png")
    app.run(debug=True)
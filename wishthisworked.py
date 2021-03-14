# actual ai 

from TwitterAPI import TwitterAPI
import geopandas as gpd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from nltk import word_tokenize
from gensim.models.wrappers import FastText 

import os
import json
import descartes
import gensim
import nltk


# fasttext setup
model = gensim.models.fasttext.load_facebook_vectors('cc.tl.300.bin')
                                        
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

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
    keywords = ["kalamidad", "tulong", "suporta"]

    response =api.request("statuses/filter", { "track":["baha", "tulong", "suporta"], "locations":[115, 5, 130, 20 ] })

    coordinates = []

    tweets = response.get_iterator()

    count = 0
    while count < 1:
        tweet = next(tweets)
        tweet_tokens = word_tokenize(tweet["text"])  

        if "place" in tweet and tweet["place"] != None:
            x, y = tweet["place"]['bounding_box']["coordinates"][0][0]
            if (x >= 115 and x <= 130 and y >= 5 and y <= 20):
                sum = 0
                for tweet_word in tweet_tokens:
                    for keyword in keywords:
                        try:
                            if tweet_word.isalpha() and tweet_word !="a" and tweet_word != "of" and tweet_word != "to" and tweet_word != "and" and model.wv.most_similar(tweet_word, keyword) > 0.45:
                                sum = sum + (int(model.most_similar(tweet_word, keyword)))
                        except Exception:
                            pass
                        if ((sum/len(tweet_tokens)) > 0.25):
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
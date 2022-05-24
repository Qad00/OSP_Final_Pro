#!/usr/bin/python3

from flask import Flask, render_template, request
from features.crawling import craw_Comments
from features.research import research
from dataset import db


app = Flask(__name__)


# go to homepage and get youtube video link
# action post
@app.route('/')
def index():
    return render_template('home_page.html')


@app.route('/result_page', methods=['POST'])
def result():
    given_url = request.form(['url'])
    # get video from youtube with given url and redirect to result page
    video = ""
    # go to crawling file and take word_cloud
    word_cloud = craw_Comments(given_url)
    # take research result
    research_res = research(given_url)


    # db manage
     
    #return data should replace: local vars to db data...
    return render_template("result_page.html", video=video, word_cloud=word_cloud, research_res=research_res)


if __name__ == '__main__':
    app.run()

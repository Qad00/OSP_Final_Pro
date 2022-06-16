#!/usr/bin/python3
<<<<<<< HEAD
import argparse
from flask import Flask, render_template, request
from features.Craw_data import Crawling as Craw_data
from features import prepro
from features.Preprocessing import Preprocessing
from models import Kkma
from dataset.knusl import KnuSL
from features.db import elasticsearch
from features import test
from features.db import emotion_analysis

app = Flask(__name__)

# BASE = http://127.0.0.1:5000


def print_crawling_result(keyword, video_data):
    i = 0
    print("keyword:  ", keyword)
    for link in video_data.keys():
        print("link{} = {},  title = {}, pic = {}, likes ={}, hits = {}".format((i + 1), link, video_data[link]['title'],
              video_data[link]['img'], video_data[link]['likes'], video_data[link]['hits']))

        i += 1


=======

import argparse
import subprocess
from flask import Flask, render_template, request
from features.Data_process.Crawling import Crawling
from features.Data_process.Preprocessing import Preprocessing
from features.db.elasticsearch import Elastic_class
# from features.db import emotion_analysis

app = Flask(__name__)
# BASE = http://127.0.0.1:5000

def print_crawling_result(keyword, video_data):
    i = 0
    print(f"keyword: {keyword}")
    for link in video_data.keys():
        print(f"link{i + 1} = {link},  title = {video_data[link]['title']}, pic = {video_data[link]['img']}, likes ={video_data[link]['likes']}, hits = {video_data[link]['hits']}")
        i += 1

>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
i = 1
j = 1
    

# home page
@app.route('/')
def index():
    global i
<<<<<<< HEAD
    crawData = Craw_data()
=======
    crawData = Crawling()
    elastic = Elastic_class(es_host=f'http://172.20.0.3:9200/')
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
    # craw title, img, link, likes, views from top 10 videos in realtime
    crawData.setHVideo()

    # temporary store link --> {title, img, likes, hits } in videos_data
    videos_data = crawData.getHVideo()
<<<<<<< HEAD
    elasticsearch.insert("home_data", i, videos_data)
    i = i + 1
    elasticsearch.search("home_data")
=======

    elastic.insert("home_data", i, videos_data)
    i = i + 1
    elastic.search("home_data")
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
    print_crawling_result("None", videos_data)

    print("Home page checked successfully")
    crawData.closeDriver()
    return render_template('home_page.html', videos_data=videos_data)

<<<<<<< HEAD
=======
# @app.route('/')
# def index():
    
#     return render_template('result_page.html')
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310

@app.route('/searched_word_result_page', methods=['GET', 'POST'])
def required_videos():
    global j
    # get word that was searched form searching field
<<<<<<< HEAD
    crawData = Craw_data()
=======
    crawData = Crawling()
    elastic = Elastic_class(es_host='http://172.20.0.3:9200/')
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
    #option = "by default"
    keyword = "By default"
    if request.method == 'POST':
        #option = request.form['selected_option']
        keyword = request.form['word_in_searching_field']
    elif request.method == 'GET':
        #option = request.args.get('selected_option')
        keyword = request.args.get('word_in_searching_field')

    # craw first 10 videos_data --> video_link, title, image, views, likes
    print("keyword:  ", keyword)
    crawData.setKVideo(keyword)
    videos_data = crawData.getKVideo()
    # store to db crawled data
<<<<<<< HEAD
    elasticsearch.insert("search_data", j, videos_data)
    j = j + 1
    elasticsearch.search("search_data")
=======
    elastic.insert("search_data", j, videos_data)
    j = j + 1
    elastic.search("search_data")
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
    
    print_crawling_result(keyword, videos_data[keyword])

    print("Searched word result page --> Success")
    crawData.closeDriver()
    print("Driver closed")
<<<<<<< HEAD
    return render_template("searched_word_result_page.html", keyword=keyword, videos_data=videos_data)


=======
    return render_template("searched_word_result_page.html", keyword=keyword, videos_data=videos_data[keyword])

#             # get research result that was done
#     research_res = research_data(crawled_data)

k = 1
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
l = 1
# run after one of video was clicked
@app.route('/result_page', methods=['GET', 'POST'])
def result():
    global k, l
    clicked_video_link = 'By default'
<<<<<<< HEAD
    craw_data = Craw_data()
    pre = Preprocessing()
=======
    craw_data = Crawling()
    pre = Preprocessing()
    elastic = Elastic_class(es_host='http://172.20.0.3:9200/')
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
    # data could be accessed in html from db
    # or return by variables from result function
    if request.method == 'POST':
        clicked_video_link = request.form.get('my_var')
    elif request.method == 'GET':
        clicked_video_link = request.args.get('my_var')

    print("Link of clicked video:  ", clicked_video_link)

    # craw comments by given link
    craw_data.setVComment(clicked_video_link)
    #temporary store in variable
    comments = craw_data.getVComment()
<<<<<<< HEAD
    el = elasticsearch.db2(clicked_video_link, comments[clicked_video_link])
    elasticsearch.insert("com_data", l, el)
    l = l + 1
    print("\n\n Comments: ")
    print(comments)
    elasticsearch.search("com_data")
=======
    el = elastic.db2(clicked_video_link, comments[clicked_video_link])
    elastic.insert("com_data", l, el)
    l = l + 1
    print("\n\n Comments: ")
    print(comments)
    elastic.search("com_data")
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310

    # Result data
    num = 0
    pn = 0
    p_percent = 0
    pos_words = []
    neg_words = []
    word_cloud = "url"
<<<<<<< HEAD
    el = elasticsearch.db3(clicked_video_link, num, pn, p_percent, pos_words, neg_words, word_cloud)
    elasticsearch.insert("result_data", k, el)
=======
    el = elastic.db3(clicked_video_link, num, pn, p_percent, pos_words, neg_words, word_cloud)
    elastic.insert("result_data", k, el)
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310
    k = k + 1
    
    craw_data.closeDriver()
    print("Research result page check -- >  Success")
    print("Driver closed")
    return render_template("result_page.html")


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="")
        parser.add_argument('--listen-port', type=str, required=True, help='Rest service listen port')
        args = parser.parse_args()
        listen_port = args.listen_port
    except Exception as e:
        print('Error: %s' % str(e))

<<<<<<< HEAD
    ipaddr = "127.0.0.1"
    print("Starting the service with ip_addr=" + ipaddr)
    app.run(debug=False, host=ipaddr, port=int(listen_port))


=======
    # Docker vs VM (Warning!!!!!)
    ipaddr=subprocess.getoutput("hostname -I").split()[0]
    # ipaddr = "127.0.0.1"
    print("Starting the service with ip_addr=" + ipaddr)
    app.run(debug=False, host=ipaddr, port=int(listen_port))
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310

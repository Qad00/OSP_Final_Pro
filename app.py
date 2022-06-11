#!/usr/bin/python3
import argparse
from flask import Flask, render_template, request
from features.Craw_data import Crawling as Craw_data
from features.db import elasticsearch

app = Flask(__name__)

# BASE = http://127.0.0.1:5000


def print_crawling_result(keyword, video_data):
    i = 0
    print("keyword:  ", keyword)
    for link in video_data.keys():
        print("link{} = {},  title = {}, pic = {}, likes ={}, hits = {}".format((i + 1), link, video_data[link]['title'],
              video_data[link]['img'], video_data[link]['likes'], video_data[link]['hits']))

        i += 1


i = 1
j = 1
    

# home page
@app.route('/')
def index():
    global i
    crawData = Craw_data()
    # craw title, img, link, likes, views from top 10 videos in realtime
    crawData.setHVideo()

    # temporary store link --> {title, img, likes, hits } in videos_data
    videos_data = crawData.getHVideo()
    elasticsearch.insert("home_data", i, videos_data)
    i = i + 1
    elasticsearch.search("home_data")
    print_crawling_result("None", videos_data)

    print("Home page checked successfully")
    crawData.closeDriver()
    return render_template('home_page.html', videos_data=videos_data)


@app.route('/searched_word_result_page', methods=['GET', 'POST'])
def required_videos():
    global j
    # get word that was searched form searching field
    crawData = Craw_data()
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
    elasticsearch.insert("search_data", j, videos_data)
    j = j + 1
    elasticsearch.search("search_data")
    
    print_crawling_result(keyword, videos_data[keyword])

    print("Searched word result page --> Success")
    crawData.closeDriver()
    print("Driver closed")
    return render_template("searched_word_result_page.html", keyword=keyword, videos_data=videos_data[keyword])


l = 1
# run after one of video was clicked
@app.route('/result_page', methods=['GET', 'POST'])
def result():
    global k, l
    clicked_video_link = 'By default'
    craw_data = Craw_data()
    pre = Preprocessing()
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
    el = elasticsearch.db2(clicked_video_link, comments[clicked_video_link])
    elasticsearch.insert("com_data", l, el)
    l = l + 1
    print("\n\n Comments: ")
    print(comments)
    elasticsearch.search("com_data")

    # Result data
    num = 0
    pn = 0
    p_percent = 0
    pos_words = []
    neg_words = []
    word_cloud = "url"
    el = elasticsearch.db3(clicked_video_link, num, pn, p_percent, pos_words, neg_words, word_cloud)
    elasticsearch.insert("result_data", k, el)
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

    ipaddr = "127.0.0.1"
    print("Starting the service with ip_addr=" + ipaddr)
    app.run(debug=False, host=ipaddr, port=int(listen_port))



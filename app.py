#!/usr/bin/python3
import argparse 
import subprocess 
from flask import Flask, render_template, request
from features.Data_process.Crawling import Crawling
from features.Data_process.Preprocessing import Preprocessing
from features.db.elasticsearch import Elastic_class


app = Flask(__name__)

# BASE = http://127.0.0.1:5000


def print_crawling_result(keyword, video_data):
    i = 0
    print("keyword:  ", keyword)
    for link in video_data.keys():
        print("link{} = {},  title = {}, pic = {}, likes ={}, hits = {}".format((i + 1), link, video_data[link]['title'],
              video_data[link]['img'], video_data[link]['likes'], video_data[link]['hits']))

        i += 1

    
# home page
@app.route('/')
def index():
    crawData = Crawling()
    elastic = Elastic_class()
    # craw title, img, link, likes, views from top 10 videos in realtime
    crawData.setHVideo()

    # temporary store link --> {title, img, likes, hits } in videos_data
    videos_data = crawData.getHVideo()

    elastic.insert("home_data", videos_data)
    #elastic.search("home_data")

    print("Home page checked successfully")
    crawData.closeDriver()
    return render_template('home_page.html', videos_data=videos_data)


@app.route('/searched_word_result_page', methods=['GET', 'POST'])
def required_videos():
    crawData = Crawling()
    elastic = Elastic_class()
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
    elastic.insert("search_data", videos_data)
    #elastic.search("search_data")
    
    #print_crawling_result(keyword, videos_data[keyword])

    print("Searched word result page --> Success")
    crawData.closeDriver()
    print("Driver closed")
    return render_template("searched_word_result_page.html", keyword=keyword, videos_data=videos_data[keyword])


# run after one of video was clicked
@app.route('/result_page', methods=['GET', 'POST'])
def result():
    clicked_video_link = 'By default'
    craw_data = Crawling()
    pre = Preprocessing()
    elastic = Elastic_class()
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
    el = elastic.db2(clicked_video_link, comments[clicked_video_link])
    elastic.insert("com_data", el)
    print("\n\n Comments: ")
    #print(comments)
    #elastic.search("com_data")

    # Result data
    num = 0
    pn = 0
    p_percent = 0
    pos_words = []
    neg_words = []
    word_cloud = "url"
    el = elastic.db3(clicked_video_link, num, pn, p_percent, pos_words, neg_words, word_cloud)
    elastic.insert("result_data", el)
    
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



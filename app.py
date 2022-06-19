#!/usr/bin/python3
import argparse 
import subprocess 
from flask import Flask, render_template, request
from features.Data_process.Crawling import Crawling
from features.Data_process.Preprocessing import Preprocessing
from features.db.elasticsearch import Elastic_class
from features.Data_process import prepro
from w_model import predict_pos
import os

app = Flask(__name__)


# BASE = http://127.0.0.1:5000

# home page
@app.route('/')
def index():
    elastic = Elastic_class()
    crawData = Crawling()
   
    #craw title, img, link, likes, views from top 10 videos in realtime
    crawData.setHVideo()
    # temporary store link --> {title, img, likes, hits } in videos_data
    videos_data = crawData.getHVideo()
    crawData.closeDriver()
    
    elastic.insert("home_data", videos_data)

    return render_template('home_page.html', videos_data=videos_data)


@app.route('/searched_word_result_page', methods=['GET', 'POST'])
def required_videos():
    # get word that was searched form searching field
    crawData = Crawling()
    elastic = Elastic_class()
    
    # option = "by default"

    keyword = "By default"
    if request.method == 'POST':
        # option = request.form['selected_option']
        keyword = request.form['word_in_searching_field']
    elif request.method == 'GET':
        # option = request.args.get('selected_option')
        keyword = request.args.get('word_in_searching_field')


    # craw first 10 videos_data --> video_link, title, image, views, likes
    crawData.setKVideo(keyword)
    videos_data = crawData.getKVideo()
    
    elastic.insert("search_data", videos_data)

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
    
    if request.method == 'POST':
        clicked_video_link = request.form.get('my_var')
    elif request.method == 'GET':
        clicked_video_link = request.args.get('my_var')

    print("Link of clicked video:  ", clicked_video_link)

    # craw comments by given link
    craw_data.setVComment(clicked_video_link)
    # temporary store in variable
    comments = craw_data.getVComment()
    
    # Elastic part
    el = elastic.db2(clicked_video_link, comments[clicked_video_link])
    elastic.insert("com_data", el)

    cleaned_comments = list()
    for com in comments[clicked_video_link]:
        t = prepro.text_preprocess(com)
        t = t.strip()
        if (len(t) != 0) and ((t != '.') or (t != '..') or (t != '...')):
            cleaned_comments.append(t)

    # Result data
    num_com, pos_list, neg_list, pos_per = predict_pos.get_res_result(cleaned_comments)
    np = 0
    word_cloud = "url"
    
    # checking results
    print("Number of comments: ", num_com)
    print("Number of positive comments: ", len(pos_list))
    print("Number of negative comments: ", len(neg_list))
    print("Number of positive comments in percent: {:.2f}%".format(pos_per))
    print("Number of negative comments in percent: {:.2f}%".format(100 - pos_per))

    # elastic 
    el1 = elastic.db3(clicked_video_link, num_com, np, pos_per, pos_list, neg_list, word_cloud)
    elastic.insert("result_data", el1)

    craw_data.closeDriver()

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



#!/usr/bin/python3

import argparse
import subprocess
from flask import Flask, render_template, request
from features.Data_process.Crawling import Crawling
from features.Data_process.Preprocessing import Preprocessing
from features.db.elasticsearch import Elastic_class
from features.Data_process.Wordcloud import Wordcloud 
from w_model import predict_pos
import json
import os

app = Flask(__name__)
sp_c = 0
elastic = Elastic_class()


# home page
@app.route('/')
def index():
    crawData = Crawling()
    
    elastic = Elastic_class()
    crawData.setHVideo()
    
    elastic.insert("home_data", crawData.getHVideo())
    crawData.closeDriver()
    

    return render_template('home_page.html', videos_data=elastic.search("home_data", "non"))


@app.route('/search_word_page', methods=['GET', 'POST'])
def required_videos():
    
    if request.method == 'POST':
        option = request.form.get('select_op')
        keyword = request.form['word_in_searching_field']
    elif request.method == 'GET':
        option = request.args.get('select_op')
        keyword = request.args.get('word_in_searching_field')

    print(option)

    crawData = Crawling()
    crawData.setKVideo(keyword)

    elastic.insert("search_data", crawData.getKVideo())

    crawData.closeDriver()
    print("Driver closed")
    
    return render_template("search_word_page.html", keyword=keyword, videos_data=elastic.search("search_data", keyword))


# run after one of video was clicked
@app.route('/result_page', methods=['GET', 'POST'])
def result():
    global sp_c 
    clicked_video_link = 'By default'
    craw_data = Crawling()
    pre = Preprocessing()
    
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

    pre.chatToSentence(comments)  
    prepro_comms = pre.getSentence() 
    
    # Result data
    num_com, pos_list, neg_list, pos_per = predict_pos.get_res_result(prepro_comms)
    np = 0
    # word cloud
    if len(pos_list) > len(neg_list):
        wordT = Wordcloud(data=pos_list, dtype="pos")
    else:
        wordT = Wordcloud(data=neg_list, dtype="neg")

    word_cloud = wordT.makeWordCloud(sp_c)
    sp_c = sp_c + 1
 
    # checking results
    #print("Number of comments: ", num_com)
    #print("Number of positive comments: ", len(pos_list))
    #print("Number of negative comments: ", len(neg_list))
    #print("Number of positive comments in percent: {:.2f}%".format(pos_per))
    #print("Number of negative comments in percent: {:.2f}%".format(100 - pos_per))

    # elastic 
    el1 = elastic.db3(clicked_video_link, num_com, np, pos_per, pos_list, neg_list, word_cloud)
    elastic.insert("result_data", el1)

    craw_data.closeDriver()
    print("Driver closed")
    t = elastic.search("result_data", clicked_video_link)
    print(t["word cloud"]) 
    print(pos_list) 
    print(neg_list) 

    return render_template("result_page.html", video_url=clicked_video_link, db=elastic.search("result_data", clicked_video_link))


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


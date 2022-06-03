#!/usr/bin/python3
import argparse
from flask import Flask, render_template, request
from features.Craw_data import Craw_data

app = Flask(__name__)

# BASE = http://127.0.0.1:5000
# init Craw_data class to start crawling
crawData = Craw_data()


# temporary storing --> test.
def print_crawling_result(keyword, video_data, link_com):
    i = 0
    print("keyword:  ", keyword)
    for link in video_data.keys():
        print("link{} = {},  title = {}, pic = {}, likes D, hits D".format((i + 1), link, video_data[link]['title'],
                        video_data[link]['img']))
        print("Comments:")
        # check correctness of links
        if link == list(link_com.keys())[i]:
            print(link, link_com[link])
        else:
            print("Incorrect matching")
        i += 1


# home page
@app.route('/')
def index():
    # craw title, img, link, likes, views from top 10 videos in realtime
    crawData.setHVideo()

    # temporary store link --> {title, img, likes, hits } in videos_data
    videos_data = crawData.getHVideo()

    # temp
    link_comment = {}
    # craw each video comments from links given above
    for link in videos_data.keys():
        crawData.setVComment(link)  # in parameters should change to take link from dic
        link_comment.update(crawData.getVComment())

    # print data to check result
    print_crawling_result("None", videos_data, link_comment)

    # do pos/neg research for all

    # sort by pos/neg result videos
    print("Home page checked successfully")
    return render_template('home_page.html')


@app.route('/searched_word_result_page', methods=['GET', 'POST'])
def required_videos():
    # get word that was searched form searching field
    if request.method == 'POST':
        keyword = request.form['word_in_searching_field']
    elif request.method == 'GET':
        keyword = request.args.get('word_in_searching_field')

    # craw first 10 videos_data --> video_link, title, image, views, likes
    crawData.setKVideo(keyword)
    # craw comments for each of videos links which was cralwed above
    videos = crawData.getKVideo()
    link_com = {}
    for tm_keyword in videos.values():
        for link in tm_keyword.keys():
            crawData.setVComment(link)  # get links from 10 crawled links and send
            # temp store in dic
            link_com.update(crawData.getVComment())

    # print stored data for testing
    print_crawling_result(keyword, videos[keyword], link_com)

    # do pos/neg research for each video with keyword and store in elasticsearch

    # sort by pos/neg result top-down

    print("Searched word result page --> Success")
    # return to searching_result page
    return render_template("searched_word_result_page.html")


# run after one of video was clicked
@app.route('/result_page')
def result():
    # data could be accessed in html from db
    # or return by variables from result function

    print("Research result page check -- >  Success")
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
    # Not work!!! need some handling
    crawData.closeDriver()
    print("Driver closed")


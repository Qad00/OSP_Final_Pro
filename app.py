#!/usr/bin/python3

from flask import Flask, render_template, request
#from features.crawling import craw_comments
#from features.comment_research import research_data
#from features.word_cloud import make_word_cloud
#from features.url_type import check_url_type
#from features.url_type import get_video_id
from features.db.elasticsearch import *

app = Flask(__name__)


# BASE = http://127.0.0.1:5000

# go to homepage and get youtube video link
# action post

# @app.route('/')
# def index():
    
#     return render_template('result_page.html')


# @app.route('/result_page', methods=['POST'])
# def result():
#     given_url = request.form(['url'])
#     # get video from youtube with given url and redirect to result page

#     # check is url is youtube type url
#     if not check_url_type(given_url):
#         # if not return 404 error to home page with explanation correct form of youtube video link
#         return "home_html", 404

#     # FIRST check db is exist such research already in db
#         # if no
#             # get video id for using in html
#     video_id = get_video_id(given_url)

#             # crawling video comments with given url
#     crawled_data = craw_comments(given_url)

#             # make word cloud from crawled data
#     word_cloud = make_word_cloud(crawled_data)

#             # get research result that was done
#     research_res = research_data(crawled_data)

#             # add new research with parameters to db

#     # return parameters and asked research, to result_page from db
#     return render_template("result_page.html", video_id=video_id, word_cloud=word_cloud, research_res=research_res)


if __name__ == '__main__':
    # test={ url:{"title":title,
    #             "image" : image,
    #             "hits":hits,
    #             "good" : good,
    #             "result number": num,
    #             "positive/negetive" : pn,
    #             "positive percent" : p_percent,
    #             "positive word": list(p_word),
    #             "negetive word": list(n_word),
    #             "word cloud" : file_path
    #         }
    #     }
    # es_host ="http://localhost:9200"
    # es = Elasticsearch(es_host)
    test=url_result("url",'title_name','image_name',1000,50,100,1,80,[1,2,3],[4,5,6],"example")
    print(insert('result',1,test))
    search('result')
    # app.run()

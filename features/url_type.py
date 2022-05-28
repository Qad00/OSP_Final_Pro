#!/usr/bin/python3
from pytube import extract
import re


# check, is it youtube video url
def check_url_type(url):
    # Types of URLs supported
    # http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
    # http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
    # http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
    # http://www.youtube.com/watch?v=0zM3nApSvMg# t=0m10s
    # http://www.youtube.com/embed/0zM3nApSvMg?rel=0
    # http://www.youtube.com/watch?v=0zM3nApSvMg
    # http://youtu.be/0zM3nApSvMg

    match_url = re.match(r'.*((youtu.be/)|(v/)|(/u/\w/)|(embed/)|(watch\?))\??v?=?([^#&?]*).*', url)
    #print(match_url)
    if match_url:
        return True
    return False


# return video_id from url
def get_video_id(url):
    return extract.video_id(url)


#test
if __name__ == '__main__':
    check_url_type("http://www.youtube.com/embed/0zM3nApSvMg?rel=0")

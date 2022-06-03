# Backend

## Crawling Class Description
1. Using Library
- "selenium"
- "webdriver_manager"
- "tqdm"

2. Constructor Parts
- Set some options before creating driver.
- Create chrome driver using "Selenium" library.

3. Crawling videos from youtube main page
- Using the setted 'url' parameter, default of url is youtube site, start crawling 10 videos in youtube site and store the result in class variable.
- Crawling target is videos title, thumbnail image, videos link(url address), the number of hits, and the number of likes.
- Whenever you need the crawled data, you can call the class method.
- The structure of crawled data
{
    "{Video Link1}" : {
        "title" : "{Video Title}",
        "img" : "{Video Thumbnail Image Link}",
        "hits" : "{Video Hits}",
        "likes" : "{Video Likes}"
    },
    "{Video Link2}" : {
        "title" : "{Video Title}",
        "img" : "{Video Thumbnail Image Link}",
        "hits" : "{Video Hits}",
        "likes" : "{Video Likes}"
    },
    ...
}

4. Crawling videos using keyword which receive from the user
- Using the given 'keyword' and 'url' parameter, default of url is youtube site, connect the youtube page at first.After that, move searched page using 'keyword' and start crawling 10 videos in the searched page. Finally, store the crawled data in class variable.
- Crawling target is videos title, thumbnail image, videos link(url address), the number of hits, and the number of likes.
- Whenever you need the crawled data, you can call the class method.
- The structure of crawled data
{
    "{keyword}" : {
        "{Video Link1}" : {
            "title" : "{Video Title}",
            "img" : "{Video Thumbnail Image}",
            "hits" : "{Video Hits}",
            "likes" : "{Video Likes}"
        },
        "{Video Link2}" : {
            "title" : "{Video Title}",
            "img" : "{Video Thumbnail Image}",
            "hits" : "{Video Hits}",
            "likes" : "{Video Likes}"
        },
        ...
    },
    "{keyword}" : {
        "{Video Link1}" : {
            "title" : "{Video Title}",
            "img" : "{Video Thumbnail Image}",
            "hits" : "{Video Hits}",
            "likes" : "{Video Likes}"
        },
        "{Video Link2}" : {
            "title" : "{Video Title}",
            "img" : "{Video Thumbnail Image}",
            "hits" : "{Video Hits}",
            "likes" : "{Video Likes}"
        },
        ...
    },
    ...
}

5. Crawling comments in the video
- Using the given 'link' and 'sc_num' parameter, link is a video address and sc_num is how many scroll the video page and default of sc_num is 60, start crawling comments in the video. Finally, store the crawled data in class variable.
- Crawling target is videos comments.
- Whenever you need the crawled data, you can call the class method.
- The structure of crawled data
{
    "{Video Link}" : [{comment1}, {comment2}, ...]
}

6. Driver close
- Why this method is needed?
When you close the driver after the crawling in each time, Session id error is arose.
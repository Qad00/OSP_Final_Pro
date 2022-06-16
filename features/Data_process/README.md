# Backend

## Crawling Class Description
<details>
<summary> Crawling Explain </summary>
<div markdown='1'>

### Using Library
- "selenium"
- "webdriver_manager"
- "tqdm"

### Structure of Crawling class
#### 1. Constructor Parts
- Set some options before creating driver.
- Create chrome driver using "Selenium" library.

#### 2. Crawling videos from youtube main page
- Using the setted 'url' parameter, default of url is youtube site, start crawling 10 videos in youtube site and store the result in class variable.
- If the video is real-time video, Crawler skip the video because we don't crawl the comments of the video.
- Crawling target is videos title, thumbnail image, videos link(url address), the number of hits, and the number of likes.
- Whenever you need the crawled data, you can call the class method.
- The structure of crawled data
```json
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
```

#### 3. Crawling videos using keyword which receive from the user
- Using the given 'keyword' and 'url' parameter, default of url is youtube site, connect the youtube page at first.After that, move searched page using 'keyword' and start crawling 10 videos in the searched page. Finally, store the crawled data in class variable.
- If the video is real-time video, Crawler skip the video because we don't crawl the comments of the video.
- Crawling target is videos title, thumbnail image, videos link(url address), the number of hits, and the number of likes.
- Whenever you need the crawled data, you can call the class method.
- The structure of crawled data
```json
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
```

#### 4. Crawling comments in the video
- Using the given 'link' and 'sc_num' parameter, link is a video address and sc_num is how many scroll the video page and default of sc_num is 60, start crawling comments in the video. Finally, store the crawled data in class variable.
- Crawling target is videos comments.
- Whenever you need the crawled data, you can call the class method.
- The structure of crawled data
```json
{
    "{Video Link}" : ["{comment1}", "{comment2}", ...]
}
```

#### 5. Driver close
- Why this method is needed?
<<<<<<< HEAD:features/README.md
When you close the driver after the crawling in each time, Session id error is arose.
=======
When you close the driver after the crawling in each time, Session id error can be arose.
</div>
</details>

## Preprocessing Class Description
<details>
<summary>Preprocessing Explain</summary>
<div markdown='1'>

### Using Library
- "re"
- "tqdm"
- "Crawling" (Option)

### Structure of Preprocessing Class
#### 1. Constructor Parts
- Define Special Characters, Emoticons (Unicode Range), Alphabet (Unicode Range)

#### 2. Data Processing Parts
- Break the comments into several sentences based on line feed and store the sentences in class variable.
- Break the sentences into several words based on white space and erase special characters or emoticons in the word. And then store the words in class variable.
- If you need the processed data, you can call the class method.
</div>
</details>
>>>>>>> dd03c63b1c7bb3773bde2959f17d6debc2cbb310:features/Data_process/README.md

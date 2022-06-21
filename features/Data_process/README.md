## Crawling Class Description
<details>
<summary> Crawling Explain </summary>
<div markdown='1'>

### Using Library
- "selenium"
- "webdriver_manager"
- "tqdm"

### Structure of Crawling class
#### 1. Part of Constructor
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

#### 3. Crawling videos using keyword given by the user
- Using the given 'keyword' and 'url' parameter, default of url is youtube site, connect the youtube page at first.After that, move searched page using 'keyword' and start crawling 10 videos in the searched page. Finally, store the crawled data in class variable.
- If the video is real-time video, Crawler skip the video because we don't crawl the comments of the video.
- If the video is "SHORTS" video, then Crawler skip the video.
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
- Using the given 'link' and 'sc_num' parameter, link is a video address and sc_num is how many scroll the video page and default of sc_num is 20, start crawling comments in the video. Finally, store the crawled data in class variable.
- Crawling target is comments of the video.
- Whenever you need the crawled data, you can call the class method.
- The structure of crawled data
```json
{
    "{Video Link}" : ["{comment1}", "{comment2}", ...]
}
```

#### 5. Closing the driver
- Close the driver used.
</div>
</details>

## Preprocessing Class Description
<details>
<summary>Preprocessing Explain</summary>
<div markdown='1'>

### Using Library
- "re"
- "tqdm"

### Structure of Preprocessing Class
#### 1. Part of Constructor
- Define Special Characters, Emoticons (Unicode Range), Alphabets, Numbers

#### 2. Processing of the comment data into sentence data
- Break the comments into several sentences based on line feed and store the sentences in class variable.
- If you need the processed data, you can call the class method.

#### 3. Processing of the sentence data into word data
- Break the sentences into several words based on white space and erase special characters or emoticons in the word. And then store the words in class variable.
- If you need the processed data, you can call the class method.
</div>
</details>

## Word Cloud Class Description
<details>
<summary> Crawling Explain </summary>
<div markdown='1'>

### Using Library
- "wordcloud"
- "konlpy"
- "collections"
- "numpy"
- "os"
- "PIL"

### Structure of Wordcloud Class
#### 1. Part of Constructor
- If a data given by parameter is exist, store the data in class variable.
- Set the image path and font path which is used to create word cloud image.
- If the data type is "pos" (positive), then set the font color "spring". If the data type is "neg" (negative), then set teh font color "PuBu".

#### 2. Creating word cloud
- Since the data received by parameter is raw data, it needs to be processed.
- Divide the data into morpheme units and then extract nouns and adjective words.
- Count the nouns and adjective words and take the top 40 words.
- Using the top 40 words, create word cloud image and store the result.
</div>
</details>
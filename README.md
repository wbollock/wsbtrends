# wsbtrends

This project is meant to show trending `$stocks` on /r/wallstreetbets in a simple manner. Ideally, it will be able to fetch trending stocks within short time frames, for example the last 30 minutes, 1 hour, etc.

## Inspiration

[Swaggy Stocks](https://swaggystocks.com/dashboard/wallstreetbets/ticker-sentiment) has done this better than I could ever hope, with sentiment analysis and neural networks.

Reddit user [pdwp90](https://www.reddit.com/user/pdwp90) also has a similar project.

## Requirements

* python-praw
* praw [Reddit API Access](https://praw.readthedocs.io/en/latest/getting_started/authentication.html)

Create a file titled `reddit_name` in your project folder with your desired Reddit username.

Another file titled `praw.ini` with your praw settings is recommended.

## Planning

~~1. Learn how to crawl reddit, specifically the DD WSB thread in this format:~~
   * ~~Appears to be two pinned threads:~~
     * [What Are Your Moves Tomorrow, November 24, 2020](https://www.reddit.com/r/wallstreetbets/comments/jzqior/what_are_your_moves_tomorrow_november_24_2020/)
     * [Daily Discussion Thread for November 24, 2020](https://www.reddit.com/r/wallstreetbets/comments/k03375/daily_discussion_thread_for_november_24_2020/)
   * On big discussion days there appear to be multiple thread parts. (**Need to aggregate data**)
        * [Daily Discussion Thread Part 5 for January 28, 2021](https://www.reddit.com/r/wallstreetbets/comments/l78za1/daily_discussion_thread_part_5_for_january_28_2021/)

2. ~~Collect comments in some format of the two daily threads.~~
3. ~~Store them somewhere.~~
4. Count for most $stock/ticker mentions.
5. Display in graph.
6. Publish graph to web page.
7. Calculate % change in last day, week?

## Features

* Obviously price of the $stock would be useful
* % change over time
* End goal is to identify the gravy trains as they're starting


        




## Resources

* [wsbtickerbot](https://github.com/RyanElliott10/wsbtickerbot) Damn, this seems to be most of what I need.
* [Swaggy Stocks Reddit Post](https://www.reddit.com/r/wallstreetbets/comments/blukl1/i_created_a_fullblown_wallstreetbets_sentiment/)
* [Reddit Scraping Guide 2018](https://www.storybench.org/how-to-scrape-reddit-with-python/)
* [PRAW Getting Started](https://praw.readthedocs.io/en/v7.1.0/getting_started/quick_start.html)
* [Reddit API Wiki](https://github.com/reddit-archive/reddit/wiki/API)
* [Python Structure](https://www.reddit.com/r/learnpython/comments/37lbe3/which_is_more_pythonic_should_i_have_a_main/)


## Technologies

* Scrapper
   * Python on cron seems to be my favorite. Wonder if I'll hit API limits. API limit seems to be 60 requests per minute.
* No more large text files. SQLite seems to be a good option for storage.
* PHP for presentation as always? I'd like to use some python graphs

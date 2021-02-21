# wsbtrends

Scraping reddit's /r/wallstreetbets to obtain occurrences of frequently mentioned stock tickers.

## Current Features

* Authenticate with reddit API and scrap two current pinned posts
* Validate actual NYSE ticker symbols
* Count their occurrences

## Requirements

1. Create a file titled `reddit_name` in your project folder with your desired Reddit username.

2. Another file titled `praw.ini` with your [praw settings](https://praw.readthedocs.io/en/latest/getting_started/authentication.html) is recommended.

3. `pip3 install -r requirements.txt`

4. MongoDB ([Arch Linux](https://aur.archlinux.org/packages/mongodb-bin/))

5. Install a cron job for every 3 hours (`crontab -l 2>/dev/null; echo "0 */3 * * * cd /full/path/to/project && python3 wsbtrends.py" | crontab -`)

## Planning

~~1. Learn how to crawl reddit, specifically the DD WSB thread in this format:~~
   * ~~Appears to be two pinned threads:~~
     * [What Are Your Moves Tomorrow, November 24, 2020](https://www.reddit.com/r/wallstreetbets/comments/jzqior/what_are_your_moves_tomorrow_november_24_2020/)
     * [Daily Discussion Thread for November 24, 2020](https://www.reddit.com/r/wallstreetbets/comments/k03375/daily_discussion_thread_for_november_24_2020/)
   * On big discussion days there appear to be multiple thread parts. (**Need to aggregate data**)
        * [Daily Discussion Thread Part 5 for January 28, 2021](https://www.reddit.com/r/wallstreetbets/comments/l78za1/daily_discussion_thread_part_5_for_january_28_2021/)

2. ~~Collect comments in some format of the two daily threads.~~
3. ~~Store them somewhere.~~
4. ~~Count for most $stock/ticker mentions.~~
5. Put in database.
6. Display in graph, grab from database.
7. Publish graph to web page. 
8. Allow user to change view, e.g mentions of GME over time. Calculate % change in last day, week
9. Verify data is correct by pointing scrapper to own subreddit with known values
10. Investigate best threads to scrape and time to scrape - are pinned posts the best answer? When is the "What are your moves tomorrow thread" generally "done"?


## Feature Goals

* Obviously price of the $stock would be useful
* % change over time
* End goal is to identify the gravy trains as they're starting
* Expand/fork for /r/cryptocurrency


## Resources and Inspiration

* [wsbtickerbot](https://github.com/RyanElliott10/wsbtickerbot)
* [Swaggy Stocks Reddit Post](https://www.reddit.com/r/wallstreetbets/comments/blukl1/i_created_a_fullblown_wallstreetbets_sentiment/)
* [Reddit Scraping Guide 2018](https://www.storybench.org/how-to-scrape-reddit-with-python/)
* [PRAW Getting Started](https://praw.readthedocs.io/en/v7.1.0/getting_started/quick_start.html)
* [Reddit API Wiki](https://github.com/reddit-archive/reddit/wiki/API)
* [Python Structure](https://www.reddit.com/r/learnpython/comments/37lbe3/which_is_more_pythonic_should_i_have_a_main/)
* Reddit user [pdwp90](https://www.reddit.com/user/pdwp90) also has a similar project.

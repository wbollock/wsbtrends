# wsbtrends

This project, which hopefully will not be quickly abandoned, is meant to show trending $stocks on /r/wallstreetbets in a simple manner. Ideally, it will be able to fetch trending stocks within short time frames, for example the last 30 minutes, 1 hour, etc.

## Inspiration

[Swaggy Stocks](https://swaggystocks.com/dashboard/wallstreetbets/ticker-sentiment) has done this better than I could ever hope, with sentiment analysis and neural networks. However, there are only metrics for the last 24 hours. I hope I don't run into an issue they encountered with getting even faster metrics.

## Planning

1. Learn how to crawl reddit, specifically the DD WSB thread in this format:
        a. Appears to be two pinned threads:
           i. [What Are Your Moves Tomorrow, November 24, 2020](https://www.reddit.com/r/wallstreetbets/comments/jzqior/what_are_your_moves_tomorrow_november_24_2020/)
           ii. [Daily Discussion Thread for November 24, 2020](https://www.reddit.com/r/wallstreetbets/comments/k03375/daily_discussion_thread_for_november_24_2020/)
        b. On big discussion days there appear to be multiple thread parts.
           i. [Daily Discussion Thread Part 5 for January 28, 2021](https://www.reddit.com/r/wallstreetbets/comments/l78za1/daily_discussion_thread_part_5_for_january_28_2021/)
        




## Resources

* [wsbtickerbot](https://github.com/RyanElliott10/wsbtickerbot) Damn, this seems to be most of what I need.
* [Swaggy Stocks Reddit Post](https://www.reddit.com/r/wallstreetbets/comments/blukl1/i_created_a_fullblown_wallstreetbets_sentiment/)
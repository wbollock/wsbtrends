#!/usr/bin/env python

# wsbtrends.py


# imports
# for reddit
import praw
# for stock info
import yfinance as yf

import re
import os

def redditAuth():
    # authenticate with Praw
    reddit = praw.Reddit("VexasAPI", user_agent="linux:wsbtrends:v1 (by /u/VexasAPI)")
    # ensure Praw stays read only
    reddit.read_only = True

    return getThread(reddit)


def getThread(reddit):
    # set sub
    subreddit = reddit.subreddit("wallstreetbets")

    #url = "https://www.reddit.com/r/wallstreetbets/comments/l7wqsm/daily_discussion_thread_for_january_29_2021_pt_ii/"
    #submission = reddit.submission(url=url)
    # submission now an object

    # thread logic: for sure would like the two pinned posts, possibly top 10 rising posts too?
    # for submission in subreddit.rising(limit=10):

    # for submission.stickied in subreddit:
        #     print(submission)

    postList = []

    for submission in subreddit.hot(limit=5):
        # usually the top 2 `hot` submissions are stickied anyway, but an extra test to ensure
        if submission.stickied == True:
            postList.append(submission.id)
        
        
    # for items in postList:
    #     print(items)

    # for dev/testing
    postList = ['kjdkdk', 'kj17ga']
    # december 24


    return getComments(postList,reddit)


def getComments(postList,reddit):

    # allows all comments to be gathered, replacing "MoreComments" with a valid object
    # literally every comment, top level and all level here
    # breadth-first iteration done with .list

    
    commentsFile = "comments.txt"
    # for dev/testing
    if os.path.exists(commentsFile):
        os.remove(commentsFile)

    # for our stickied threads
    for item in postList:
        id = item

        # submission = id
        submission = reddit.submission(id=id)

        print("Writing to file...", item, submission.title)

        submission.comments.replace_more(limit=5)
        # for testing
        # submission.comments.replace_more(limit=5)

        for comment in submission.comments.list():
            file = open(commentsFile, "a")
            file.write(comment.body)
            file.close()

    # just top level comments
    # submission.comments.replace_more(limit=0)
    # for top_level_comment in submission.comments:
    #     print(top_level_comment.body)

    # print("getComments")

    return getTicker(commentsFile)


def getTicker(commentsFile):
    # extract ticker symbols from comments
    # yfinance seems to be the way to go for price
    # msft = yf.Ticker("MSFT")
    # msft.info for a dict of everything
    # msft.info['ask'] for current price?
    # msft.info['bid] for current.. buying price?
    tickerFile =  "tickers.txt"
    

    # for dev/testing
    if os.path.exists(tickerFile):
        os.remove(tickerFile)

    with open(commentsFile) as c:
        for line in c:
            match = re.findall(r'\b[A-Z]{3}\b[.!?]?',line)
            # if match contains data
            if match:
                

                for item in match:
                    file = open(tickerFile, "a")
                    file.write(item)
                    file.close
                        
           
    
    



def main():
   redditAuth()

    

    
if __name__ == "__main__":
    main()
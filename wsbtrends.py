#!/usr/bin/env python

# wsbtrends.py


# imports
# for reddit
import praw
# for stock info
import yfinance as yf

# yfinance seems to be the way to go for price
    # msft = yf.Ticker("MSFT")
    # msft.info for a dict of everything
    # msft.info['ask'] for current price?
    # msft.info['bid] for current.. buying price?

import re
import os

import numpy as np

from collections import Counter

# Major TODOs
# TODO: get rid of my awful dependencies on files and just hold stuff in memory

def redditAuth():
    # authenticate with Praw
    # create file "reddit_name"
    redditFileName = "reddit_name"

    with open(redditFileName, 'r') as file:
        redditUsername = file.read().replace('\n', '')

    # alex you can keep it linux don't change it you weeb
    userAgent = "linux:wsbtrends:v1 (by /u/" + redditUsername + ")"

    # https://praw.readthedocs.io/en/latest/getting_started/authentication.html
    reddit = praw.Reddit(redditUsername, user_agent=userAgent)
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

    for submission in subreddit.hot(limit=2):
        # usually the top 2 `hot` submissions are stickied anyway, but an extra test to ensure
        if submission.stickied == True:
            postList.append(submission.id)
        
        
    # for items in postList:
    #     print(items)

    # for dev/testing
    #postList = ['kjdkdk', 'kj17ga']
    # december 24


    return getComments(postList,reddit)


def getComments(postList,reddit):

    # allows all comments to be gathered, replacing "MoreComments" with a valid object
    # literally every comment, top level and all level here
    # breadth-first iteration done with .list

    
    commentsFile = "comments.txt"
    
    if os.path.exists(commentsFile):
        os.remove(commentsFile)

    # for our stickied threads
    for item in postList:
        id = item

        # submission = id
        submission = reddit.submission(id=id)

        print("Writing to file...", item, submission.title)

        # limit=None is all comments
        submission.comments.replace_more(limit=None)
        # for testing
        # submission.comments.replace_more(limit=5)

        for comment in submission.comments.list():
            try: 
                #Going to run into Unicode Encode Errors for some comments TODO: Look into Unicode Encode Errors
                # must be some lame Windows thing
                file = open(commentsFile, "a")
                file.write(comment.body)
                file.close()
            except UnicodeEncodeError:
                print(str(comment) + " couldn't be encoded.")

    # just top level comments
    # submission.comments.replace_more(limit=0)
    # for top_level_comment in submission.comments:
    #     print(top_level_comment.body)

    # print("getComments")

    return getTicker(commentsFile)


def getTicker(commentsFile):
    # extract ticker symbols from comments
    # still needed with NYSE file because we really only want 3-5 character, usual tickers

    tickerFile =  "tickers.txt"
    tickerList = []

    # credit: https://github.com/RyanElliott10/wsbtickerbot/blob/master/wsbtickerbot.py
    # common words on WSB to ignore
    
    blacklist_words = [
      "YOLO", "TOS", "CEO", "CFO", "CTO", "DD", "BTFD", "WSB", "OK", "RH",
      "KYS", "FD", "TYS", "US", "USA", "IT", "ATH", "RIP", "BMW", "GDP",
      "OTM", "ATM", "ITM", "IMO", "LOL", "DOJ", "BE", "PR", "PC", "ICE",
      "TYS", "ISIS", "PRAY", "PT", "FBI", "SEC", "GOD", "NOT", "POS", "COD",
      "AYYMD", "FOMO", "TL;DR", "EDIT", "STILL", "LGMA", "WTF", "RAW", "PM",
      "LMAO", "LMFAO", "ROFL", "EZ", "RED", "BEZOS", "TICK", "IS", "DOW"
      "AM", "PM", "LPT", "GOAT", "FL", "CA", "IL", "PDFUA", "MACD", "HQ",
      "OP", "DJIA", "PS", "AH", "TL", "DR", "JAN", "FEB", "JUL", "AUG",
      "SEP", "SEPT", "OCT", "NOV", "DEC", "FDA", "IV", "ER", "IPO", "RISE"
      "IPA", "URL", "MILF", "BUT", "SSN", "FIFA", "USD", "CPU", "AT",
      "GG", "ELON", "GOP", "IPO", "WSB", "HIS", "THE", "ARK", "FUCK"
   ]
    

    # for dev/testing
    if os.path.exists(tickerFile):
        os.remove(tickerFile)

    # TODO: thoughts on only limiting to 3-5 character tickers? filters out a lot of stuff like OR, ALL, 

    # TODO: clear special characters like BABA. (the period)

    
    with open(commentsFile) as c:
        for line in c:
            match = re.findall(r'\b[A-Z]{3,5}\b[.!?]?',line)
            # if match contains data
            if match:
                # subtract from blacklist
                match = list(set(match) - set(blacklist_words))
                
                # filter out any non-chars and keep spaces
                # match is a list of strs from one line
                # https://stackoverflow.com/questions/55902042/python-keep-only-alphanumeric-and-space-and-ignore-non-ascii/55902074
                match = [re.sub(r'[^A-Za-z0-9 ]+', '', x) for x in match]
                

                for item in match:
                    # file = open(tickerFile, "a")
                    # file.write(item)
                    # file.write(' ')
                    # file.close
                    tickerList.append(item)

    return validateTicker(tickerList)
                        

def validateTicker(tickerList):
    # test if it's a valid ticker

    

    # validFile = "validTickers.txt"
    # if os.path.exists(validFile):
    #     os.remove(validFile)

    validList = []

    # some issues with the list.. stuff like WOW and FOR and ALL and OR are included
    NYSETicker = "NYSE.txt" #Pre-generated file TODO: Have file update when script runs and Alex tell me how you got it
    validTicker = {}
    notcounted = {}

    with open(NYSETicker, "r") as q:
        for line in q:
            validTicker[line.rstrip('\n')] = True
      

    
    for line in tickerList: #Not O(N^2) because it is only one line
        # for each individual "ticker"
        for word in line.split():
            # attempt to validate ticker
            if validTicker.get(word, False):
                if notcounted.get(word, True):
                    notcounted[word] = False
                    # write successful matches to list
                    validList.append(word)
                    #file = open(validFile, "a")
                    #file.write(word)
                    #file.write(" ")
                    #file.close()


    return countTickers(validList)
        

def countTickers(validList):
    # get count of most used tickers

   
    # https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
    # Counter does everything in a nice json-esque format
    print(Counter(validList))

    countFile = "output.txt"
    if os.path.exists(countFile):
        os.remove(countFile)

    with open(countFile, "a") as file:
        file.write(Counter(validList))
        file.close()

def main():
   redditAuth()
    
if __name__ == "__main__":
    main()
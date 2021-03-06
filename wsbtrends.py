#!/usr/bin/env python

# wsbtrends.py


# imports
# for reddit
import praw
import re
import os
import numpy as np
from collections import Counter
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime

# for stock info
#import yfinance as yf
# yfinance seems to be the way to go for price
# msft = yf.Ticker("MSFT")
# msft.info for a dict of everything
# msft.info['ask'] for current price?
# msft.info['bid] for current.. buying price?

# Major TODOs
# 1. Speed kinda sucks


# Global.. is this sinful?
logStart = datetime.now().strftime("%Y_%m_%d-%H:%M:%S")
start = datetime.now()

# relative paths from current working directory
base_path = Path(__file__).parent
logPath = str(base_path) + "/logs/" + "wsbtrends_" + str(logStart) + ".log"

def logCreate():
    # create log file for writing throughout program
    # log run start
    with open(logPath, 'w') as f:
        f.write("wsbtrends.py - start of run:\n")
        f.write(str(logStart))
        f.write("\n")
        f.close()

    return redditAuth()

def redditAuth():
    # authenticate with Praw
    
    redditFileName = str(base_path) + "/config/reddit_name"
    redditFilePath = Path(str(base_path) + "/config/reddit_name")

    # first run detection
    # if file exists
    # **must configure praw.ini also**
    if not redditFilePath.is_file():
        print("\n")
        print("First run detected.")
        print("Please enter desired Reddit username to interact with the Reddit API.")
        print("**Configure praw.ini too**.")
        print("\n")
        newuser = input("Username: ")
        with open(redditFileName, "w") as f:
            f.write(newuser)
            f.close()

        with open(logPath, 'a') as f:
            f.write("Error: " + redditFileName + " not found.")
            f.close()

        

    with open(redditFileName, 'r') as file:
        redditUsername = file.read().replace('\n', '')

    # alex you can keep it linux don't change it you weeb
    userAgent = "linux:wsbtrends:v1 (by /u/" + redditUsername + ")"

    # https://praw.readthedocs.io/en/latest/getting_started/authentication.html
    reddit = praw.Reddit(redditUsername, user_agent=userAgent)
    reddit.read_only = True

    return getThread(reddit)


def getThread(reddit):
    # set sub
    subreddit = reddit.subreddit("wallstreetbets")

    # thread logic: for sure would like the two pinned posts, possibly top 10 rising posts too?
    # for submission in subreddit.rising(limit=10):

    postList = []

    for submission in subreddit.hot(limit=2):
        # usually the top 2 `hot` submissions are stickied anyway, but an extra test to ensure
        if submission.stickied == True:
            postList.append(submission.id)
        

    # for dev/testing
    # postList = ['kjdkdk', 'kj17ga']
    # december 24 posts


    return getComments(postList,reddit)


def getComments(postList,reddit):

    # allows all comments to be gathered, replacing "MoreComments" with a valid object
    
    # breadth-first iteration done with .list

    commentsList = []

    # for stickied threads
    for item in postList:
        id = item

        # submission = id
        submission = reddit.submission(id=id)

        print("Analyzing...", submission.title)

        with open(logPath, 'a') as f:
            f.write("Scrapping: " + submission.title + "\n")
            f.close()

        # limit=None is all top-level comments
        submission.comments.replace_more(limit=None)

        # for testing
        # submission.comments.replace_more(limit=2)


        for comment in submission.comments.list():
            try: 
                #Going to run into Unicode Encode Errors for some comments TODO: Look into Unicode Encode Errors
                # must be some lame Windows thing
                commentsList.append(comment.body)
            except UnicodeEncodeError:
                #print(str(comment) + " couldn't be encoded.")
                with open(logPath, 'a') as f:
                    f.write(str(comment) + " couldn't be encoded.")
                    f.close()

    
    return getTicker(commentsList)


def getTicker(commentsList):
    # extract ticker symbols from comments
    # still needed with NYSE file because we really only want 3-5 character, usual tickers

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
      "GG", "ELON", "GOP", "IPO", "WSB", "HIS", "THE", "ARK", "FUCK", "FOR"
   ]
    

  
    #with open(commentsList) as c:
    for line in commentsList:
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
                tickerList.append(item)


    
    return validateTicker(tickerList)
                        

def validateTicker(tickerList):
    # test if it's a valid ticker

    validList = []

    # some issues with the list.. stuff like WOW and FOR and ALL and OR are included
    # TODO: Have file update when script runs and Alex tell me how you got it
    NYSETicker = "stocks/NYSE.txt" #Pre-generated file 
    
    validTicker = {}
    

    with open(NYSETicker, "r") as q:
        for line in q:
            validTicker[line.rstrip('\n')] = True
      

    for line in tickerList: #Not O(N^2) because it is only one line
        # for each individual "ticker"
        for word in line.split():
            # attempt to validate ticker
            if validTicker.get(word, False):
                validList.append(word)
                    

    return database_insert(validList)
        

def database_insert(validList):
    # get count of most used tickers

    # https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
    # Counter does everything in a nice json-esque format
    
    occurDict = dict(Counter(validList))
    tickerDict = {}

    # add datetime to our dict
    now = datetime.now()
    #print(now)

    # goal is "Ticker" : PLTR, "AMC" : 8, "GME" : 52}

    # connect to mongodb
    client = MongoClient()
    # default host/port
    wsb_db = client["wsbtrends"]
    wsb_collection = wsb_db["tickers"]

    # convert native Counter dict to a more usable format
    for key, value in occurDict.items():
        # print(key,value)
        # tickerDict[key] = {}
        # tickerDict[key]['Ticker'] = key
        # tickerDict[key]['Count'] = value
        # tickerDict[key]['Datetime'] = now

        tickerDict['Ticker'] = key
        tickerDict['Count'] = value
        tickerDict['Datetime'] = now
        wsb_collection.insert_one(tickerDict)
        tickerDict = {}

    print("Done, inserted into mongo")

    
    # adds "Datetime" : ISODate("2021-02-18T19:14:19.098Z") }
    with open(logPath, 'a') as f:
        f.write("\nInserted values into MongoDB at " + str(now))
        f.close()


    timeElapsed = now - start
    
    with open(logPath, 'a') as f:
        f.write("\nTime elapsed: " + str(timeElapsed))
        f.close()
 

    # more example commands for now because my mongo is rusty
    # find GME at 185
    # db.tickers.find({"Ticker":"GME", "Count":185})

    # find where GME is greater than 90
    # db.tickers.find({"Ticker":"GME", "Count": {$gt: 90}})

    # remove all objects
    # db.tickers.remove({})

    # sort by highest numbers in "Count"
    # db.tickers.find().sort({"Count":-1})


def main():
   logCreate()
    
if __name__ == "__main__":
    main()

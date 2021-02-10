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
    reddit = praw.Reddit("EagleEyeAPI", user_agent="windows:wsbtrends:v1 (by /u/EagleEyeAPI)") #TODO: Read from local file so we don't have to switch out on every pull
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
            try: #Going to run into Unicode Encode Errors for some comments TODO: Look into Unicode Encode Errors
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
    # yfinance seems to be the way to go for price
    # msft = yf.Ticker("MSFT")
    # msft.info for a dict of everything
    # msft.info['ask'] for current price?
    # msft.info['bid] for current.. buying price?
    tickerFile =  "tickers.txt"

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


    # TODO: improve regex
    # test regex more
    # right now {3,4} matches 3-4 character TICKERS
    # not 1,2, or 5 letter tickers
    # e.g KO = Coca-Cola
    # C = Citigroup
    # BRK.A = Berkshire

    # TODO: clear special characters like BABA. (the period)

    

    
    with open(commentsFile) as c:
        for line in c:
            match = re.findall(r'\b[A-Z]{3,4}\b[.!?]?',line)
            # if match contains data
            if match:
                # subtract from blacklist
                match = list(set(match) - set(blacklist_words))


                for item in match:
                    file = open(tickerFile, "a")
                    file.write(item)
                    file.write(' ')
                    file.close

    return validateTicker(tickerFile)
                        

def validateTicker(tickerFile):
    # test if it's a valid ticker
    print("Entering Testing")
    validFile = "validTickers.txt"
    NYSETicker = "NYSE.txt" #Pre-generated file TODO: Have file update when script runs
    validTicker = {}
    notcounted = {}
    with open(NYSETicker, "r") as q:
        print("Opened NYSE.txt")
        for line in q:
            validTicker[line.rstrip('\n')] = True
        print(validTicker)
    with open(tickerFile, "r") as t:
                for line in t: #Not O(N^2) because it is only one line
                    # for each individual "ticker"
                    for word in line.split():
                        # attempt to validate ticker
                        if validTicker.get(word, False):
                            if notcounted.get(word, True):
                                notcounted[word] = False
                                file = open(validFile, "a")
                                file.write(word)
                                file.write(" ")
                                file.close()
        
    
    



def main():
   redditAuth()

    

    
if __name__ == "__main__":
    main()
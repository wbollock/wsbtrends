#!/usr/bin/env python

# wsbtrends.py


# imports
import praw



def main():
    reddit = praw.Reddit("VexasAPI", user_agent="linux:wsbtrends:v1 (by /u/VexasAPI)")
    print(reddit.read_only)


    for submission in reddit.subreddit("learnpython").hot(limit=10):
        print(submission.title)
if __name__ == "__main__":
    main()
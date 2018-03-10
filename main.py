#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, praw, requests, os, glob, sys, time, tweepy

def downloadImage(imageUrl, fileName):
    response = requests.get(imageUrl)

    if response.status_code == 200:
        print('Downloading %s...' % (fileName))

        with open("imgs/" + fileName, 'wb') as fo: #grava o arquivo da imagem em disco
            for chunk in response.iter_content(4096):
                fo.write(chunk)
    elif response.status_code > 299:
        print('Error downloading %s...' % (fileName))

def posted(post_id):
    #access our line oriented database
    database = file('imgs/record.txt')
    found = False
    for line in database:
        if post_id in line:
            print('Image '+ post_id + ' already posted, skipping...')
            return True
    return False

##############Twitter auth
CONSUMER_KEY = "XXXXXXXXXXXXXXXXXXX"
CONSUMER_SECRET = "XXXXXXXXXXXXXXXXXXX"
ACCESS_KEY = "XXXXXXXXXXXXXXXXXXX"
ACCESS_SECRET = "XXXXXXXXXXXXXXXXXXX"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter = tweepy.API(auth)

##############Reddit auth
reddit = praw.Reddit(client_id='XXXXXXXXXXXXXXX',
                     client_secret='XXXXXXXXXXXXXXX',
                     password='p455w0rd',
                     user_agent='testscript by /u/beijoslucas',
                     username='beijoslucas')

subreddit = reddit.subreddit('ArtPorn')

while True:
    redditSuccess = False
    while redditSuccess == False:
        try:
            redditSuccess = True
            submissions = subreddit.hot(limit=100)
        except:
            redditSuccess = False
            print('ERROR: Could not get Reddit submission. Trying again in 60 seconds...')
            sleep(60)
    redditSuccess = False

    submissionBuffer = []
#Save new submissions in a buffer
    for submission in submissions:
        if posted(submission.id):
            continue

        if ".jpg" not in submission.url:
            print ('Submission ' + submission.id + ' is not postable...         Skipping.')
            continue # skip non image url submissions

        submissionBuffer.append(submission)
        print("Appended post " + submission.id)

#Consume Buffer
    for submission in submissionBuffer:
        print
        print("Posting " + submission.id)
        print(submission.url)
        title = submission.title
        print(title)

        fileName = '%s.jpg' % submission.id
        downloadImage(submission.url, fileName)

        #write post ID on our database
        with open("imgs/record.txt", "a") as myfile:
            myfile.write(submission.id + '\n')

        try:
            twitter.update_with_media("imgs/"+fileName, title)
            os.remove("imgs/"+fileName)
        except:
            print("ERROR: Could not post this image. Maybe the file is too big. Continuing...")
            os.remove("imgs/"+fileName)
            continue

        time.sleep(2000) #Post every X seconds

    print("New cycle!")

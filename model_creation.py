###################################################
# File Name: model_creation.py                    #
# Creation Date: 25 June 2019                     #
# Author: Liyogar B                               #
# Rev History                                     #
# 25/6/2019 - Liyogar B - Initial version         #
# 26/6/2019 - Rishabh A - Preprocessing           #
###################################################

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os.path
from os import path
import time

import preprocessor
import model

# define API Keys
consumer_key = 'dHqOs9nhIPvsrQB3XgM24q8MD'
consumer_secret = '4eEpERpqaXsv0squUMbEZ7zMWkPLtNU7PyYpyaSJCwUi5KCbhF'
access_token = '1143039002150260736-WaTDkw2y9BTDpXskzhZzfpMJ5PvUQi'
access_secret = 'uAdRRhrzOp4WQ6Su6L4FFPL3Xvizc3XjaSoBxe1wRbojw'

class StdOutListener(StreamListener):

    def __init__(self,record_limit=1000):
        self.counter = 0
        self.records = record_limit

    def on_data(self, data):
        if(self.counter<self.records):
            self.counter+=1
            with open('data/tweetdata'+str(self.records)+'.txt','a') as tf:
                tf.write(data)
            print(self.counter, self.records)
            return True
        else:
            #print("Completed")
            return False

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

#Download dataset from twitter
    train_size = 500
	
	#Step 1 delete data file if exists
    if(path.exists('data/tweetdata'+str(train_size)+'.txt')):
        os.remove('data/tweetdata'+str(train_size)+'.txt')
        print("Step 1: File Deleted!")
	#Step 2 Create file
    f= open('data/tweetdata'+ str(train_size)+'.txt',"w+")
    f.close()
	
    print("Step 2: File created")

    l = StdOutListener(train_size)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    print("Step 3: Downloading data")
    stream = Stream(auth, l)

    stream.filter(track=['depression', 'anxiety', 'mental health', 'suicide', 'stress', 'sad'])
	

    print("Downloading data finished")
	
# Preprocessing training data
    print("Step 4: Preprocessing training data")
    preprocessor.runall('data/tweetdata'+str(train_size)+'.txt')
    print("Preprocessing Done")
    print("Step 5: Creating and Saving Model")
    model.createModel('data/tweetdata'+str(train_size)+'.txt', 'processed_data/output.xlsx')

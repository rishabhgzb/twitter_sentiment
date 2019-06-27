###################################################
# File Name: model_creation.py                    #
# Creation Date: 27 June 2019                     #
# Authors:                                        #
#           Liyogar B,                            #
#           Rishabh A,                            #
#           Sudeep V,                             #
#           Mayank K                              #
###################################################

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os.path
from os import path
import time

import preprocessor
import model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn import metrics

# define API Keys
consumer_key = 'dHqOs9nhIPvsrQB3XgM24q8MD'
consumer_secret = '4eEpERpqaXsv0squUMbEZ7zMWkPLtNU7PyYpyaSJCwUi5KCbhF'
access_token = '1143039002150260736-WaTDkw2y9BTDpXskzhZzfpMJ5PvUQi'
access_secret = 'uAdRRhrzOp4WQ6Su6L4FFPL3Xvizc3XjaSoBxe1wRbojw'

class StdOutListener(StreamListener):

    def __init__(self,model,vectr):
        self.model = model
        self.vectr = vectr #CountVectorizer(stop_words='english') #vectr
		
		Counter_positive = 0
		Counter_Negative = 0
		Counter_neutral = 0

    def on_data(self, data):
        #msg = "You are so stupid."
        with open('data/inp.txt','w') as tf:
            tf.write(data)
            #tf.close()
        #print(data)
        x = preprocessor.getTweetText('data/inp.txt')
        print("--------------------------------------------------")
        print(x[0])
        print("--------------------------------------------------")
        #print(x[0])
        inputdtree= self.vectr.transform(x)
        predictt = self.model.predict(inputdtree)
    
        if predictt == 1:
            predictt = "Positive"
			Counter_positive += 1
        elif predictt == 0:
            predictt = "Neutral"
			Counter_neutral+=1
        elif predictt == -1:
            predictt = "Negative"
			Counter_Negative+=1
        else:
            print("Nothing")
    
        print("\n*****************")
        print(predictt)
        print("*****************")
		
		#CreatePlot(Counter_positive, Counter_neutral, Counter_Negative)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    print("Loading pickel")
    dt = joblib.load('models/dTree.pkl')
    print("Model Loaded successfully")

    vectorizer = joblib.load('models/vectr.pkl')
	#CountVectorizer(stop_words='english')
	#joblib.load('models/vectr.pkl')#CountVectorizer(stop_words='english')
	
    #Step 1 delete data file if exists
    if(path.exists('data/inp.txt')):
        os.remove('data/inp.txt')
        print("Step 1: File Deleted!")
	#Step 2 Create file
    f= open('data/inp.txt',"w+")
    f.close()

    l = StdOutListener(dt,vectorizer)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    print("Step 3: Downloading data")
    stream = Stream(auth, l)

    stream.filter(track=['depression', 'anxiety', 'mental health', 'suicide', 'stress', 'sad'])
	
# Preprocessing training data
##    print("Step 4: Preprocessing training data")
##    preprocessor.runall('data/tweetdata'+str(train_size)+'.txt')
##    print("Preprocessing Done")
##    print("Step 5: Creating and Saving Model")
##    model.createModel('data/tweetdata'+str(train_size)+'.txt', 'processed_data/output.xlsx')

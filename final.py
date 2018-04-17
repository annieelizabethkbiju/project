import requests
import sys
import numpy as np
import tweepy
import os

from keras.models import Sequential
from keras.layers import Dense
from textblob import TextBlob

consumer_key = "JqLBxM2b9bpQpezpsy15iLYzb"
comsumer_secret = "6fYANAhQJa2XLu4DFN4LRQBuoGlAglsWAdaEqH0JnbcQD1el2K"
access_token = "950991446097702912-kAmetaL4oqIPo70ppd5BWEJpXfVwinF"
access_secret = "Tpe4hh2CmlOhCHhJG2jIX0Qwzs2C7eWXcqCBTEjU7nOql"
login = tweepy.OAuthHandler(consumer_key, comsumer_secret)
login.set_access_token(access_token, access_secret)
user = tweepy.API(login)

file = 'final.csv'

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


#company = get_symbol("AAPL")

#print(company)
def sentiment(quote, num):
    tweet_list = user.search(get_symbol(quote), count = num)
    positive = 0
    null = 0
    for tweet in tweet_list:
        check = TextBlob(tweet.text).sentiment
        if check.subjectivity == 0:
            null += 1
            next
        if check.polarity > 0:
            positive += 1

    if positive > ((num - null)/2):
        return True
        
def predict():
    data = []
    with open(file) as f:
        for num, line in enumerate(f):
            if num != 0:
                data.append(float(line.split(',')[1]))
    data = np.array(data)

    def create_set(data):
        datax = [data[n+1] for n in range(len(data)-2)]
        return np.array(datax), data[2:]

    trainx, trainy = create_set(data)

    classifier = Sequential()
    classifier.add(Dense(8, input_dim = 1, activation = 'relu'))
    classifier.add(Dense(1))
    classifier.compile(loss = 'mean_squared_error', optimizer = 'adam')
    classifier.fit(trainx, trainy, nb_epoch= 200, batch_size = 2, verbose = 1)

    prediction = classifier.predict(np.array([data[0]]))
    return 'from %s to %s' % (data[0], prediction[0][0])        
        
quote = input('Enter stock quote: ').upper()



if not sentiment(quote, num = 100):
    print ('This stock has bad sentiment')
else:
    print ('This stock has good sentiment')
    
print(predict())

os.remove(file)    

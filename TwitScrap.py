#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#import re
#import os

def WriteTweet(Tweet):
        outfile = open("Tweets.txt", "a")
        outfile.write(Tweet)
        outfile.close()


#Variables that contains the user credentials to access Twitter API 
access_token = "825398905294692352-YAPcT9YM2ASFPqwRRrGDGfmtcCHYtxn"
access_token_secret = "Tdz31EiT2OhaNHjoLYXwi2Oa5UE6HTiPUvv0BqcNtZl0N"
consumer_key = "FXnxp52EFcFkYhDogBOk4xGcx"
consumer_secret = "iTjp6oNDntbKRjFk6V0BAH673oCQrtxUGpj7LnCaT7WkYsFf9w"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        WriteTweet(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    ##l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    for status in tweepy.Cursor(api.home_timeline).items(10):
            # Process a single status
            print(status.text)

    
    ##stream = Stream(auth, l)

    

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    ##stream.filter(track=['tsla', 'trump', 'rubysadsadsadsad'])

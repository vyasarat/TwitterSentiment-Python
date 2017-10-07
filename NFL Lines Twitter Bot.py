from bs4 import BeautifulSoup
from urllib import request
import pytz
from datetime import datetime
import os
import time
import tweepy
from tweepy import OAuthHandler
import numpy as np
import pandas as pd

class TwitterClient(object):
    '''
        Generic Twitter Class for sentiment analysis.
        '''
    def __init__(self):
        '''
            Class constructor or initialization method.
            '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 't6WmHDCTHy50ZQwXm8rDlXUtx'
        consumer_secret = 'sWyUUatixPVgJLwWg8e1Qa66lmMTFP5d7TfFp479jzZrXm6Zqa'
        access_token = '916520800777326593-wq1mAk9h07WngMLMgdJ3nksuFNWN3IE'
        access_token_secret = '11cs6fe0iok9gx3KKwtAXEPe2KWZxL8NltKz8ON1VSYS7'
        
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
    
    def post_tweet(self, tweet_text):
        try:
            self.api.update_status (tweet_text[0:140])
        except:
            X=1

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    #Set time interval for comparing line moves in MINUTES here
    TimeInterval = 15
    #Set number of minutes to sleep between pulls here
    SleepTime = 15
    
    #Scrape lines from ESPN
    while True:
        BASE_URL = "http://www.espn.com/nfl/lines"
        with request.urlopen(BASE_URL) as response:
            html = response.read()
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", { "class" : "tablehead" })
        
        tz = pytz.timezone('America/New_York')
        PullTime = datetime.now(tz).isoformat(timespec='seconds')
        
        #outputfilename = "C:\\Users\\Viraj\\Documents\\Football Lines Analysis\\Lines.txt"
        outputfilename = "C:\\Users\\Viraj\\Dropbox\\Public\\Lines.txt"
        #outputfilename = "Lines.txt"
        
        #If output file doesnt exist, then create it
        if os.path.isfile(outputfilename ) == False:
            HeaderFile = open(outputfilename ,"w")
            HeaderFile.write("Log_Time\t"+"Game\tSource\tLine\tOverUnder\tHomeTeam\tAwayTeam\tFavorite\tUnderdog\n")
            HeaderFile.close()
        #setup output file for appending if it exists
        outfile = open(outputfilename , "a")
        #parse HTML
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            c0 = cells[0].find(text=True)
            if len(cells) == 1 and len(c0) > 30:
                game = c0
                AwayTeam = game[0:game.index(' at')]
                HomeTeam = game[game.index(' at')+4:game.index(' -')]
            #print(HomeTeam,AwayTeam)
            elif len(cells) == 9:
                source = cells[0].find(text=True)
                Line = cells[1].find(text=True)
                #AwayTeam = cells[3].find(text=True)
                #AwayTeam = AwayTeam[:AwayTeam.index(':')]
                OverUnder = cells[5].find(text=True)
                OverUnder = OverUnder[:OverUnder.index(" ")]
                
                if float(Line) > 0:
                    Favorite = HomeTeam
                    Underdog = AwayTeam
                elif float(Line) < 0:
                    Favorite = AwayTeam
                    Underdog = HomeTeam
                else:
                    Favorite = 'Pickem'
                    HomeTeam = 'Pickem'
            elif len(cells) == 2 and cells[1].find(text=True)[:3] == 'o: ':
                #print (datetime.now(tz).isoformat(timespec='minutes'),"|",game,"|",source,"|",abs(float(Line)),"|",
                #       HomeTeam,"|",OverUnder,"|",HomeTeam,"|",AwayTeam,"|",Favorite,"|",Underdog)
                outfile.write(PullTime +"\t"+ game +"\t"+ source +"\t"+
                              str(abs(float(Line))) +"\t"+ OverUnder + "\t"+ HomeTeam + "\t"+ AwayTeam +'\t'+ Favorite +'\t'+ Underdog + '\n')
        outfile.close()
        #Ready to analyze data

        df = pd.read_csv(outputfilename,sep="\t")
        df['Time'] = pd.to_datetime(df['Log_Time'])

        
        #get unique times
        Times_df = pd.DataFrame(df.Log_Time.unique())
        Times_df.columns = ['Time']
        
        Times_df['Time'] = pd.to_datetime(Times_df['Time']) #convert to datetime data type
        
        MaxTime = Times_df.Time.max()
        
        Times_df['TimeDiff'] = (MaxTime - Times_df['Time']).astype('timedelta64[m]') #find minutes between two times
        
        #find closes time between that is at least time interval away
        TargetTime = Times_df.query("TimeDiff >= "+ str(TimeInterval)).Time.max()
        
        #q = "Time = "+MaxTime
        Current_df = df[(df['Time']==MaxTime)]
        Old_df    = df[(df['Time']==TargetTime)]
        
        Output_df = pd.merge(Current_df,Old_df,on = ['Game','Source'])
        Output_df['LineChange'] = Output_df.Line_x - Output_df.Line_y
        
        Output_df = Output_df.query("LineChange != 0")
        
        Output_df = Output_df.reset_index()
        
        for  idx,row in Output_df.iterrows():
            tweet = ('.@vrbaba Line moved '+ str(row.Line_y) + ' to '+str(row.Line_x)+'(last '+str(TimeInterval)+'mins:'+row.Source +') Fav:'+row.Favorite_x[:3]+'|OU:'+str(row.OverUnder_x)+
                 '('+row.Game.replace(" at ","@").replace(" ","")+')')
            tweets = api.post_tweet(tweet)
        time.sleep(SleepTime*60)

if __name__ == "__main__":
    # calling main function
    main()

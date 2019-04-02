import tweepy
CONSUMER_KEY = 'EQxFiVurRxZRKZzH4tJ2PtsX8'
CONSUMER_SECRET = '59WSgueMvx7VUbuYywwC6rqwdlLUkc0yufiTnITvgmPJAN9RzE'
ACCESS_TOKEN = "349586645-4e7WmYpjvzKUmsKh3C9pNyv0QzlbVB80nlvR4q02"
ACCESS_TOKEN_SECRET = "qblYvvigttmP5elDFMsIJacO7gOknN794ubMThlyV0pfj"
auth = tweepy.OAuthHandler('EQxFiVurRxZRKZzH4tJ2PtsX8', '59WSgueMvx7VUbuYywwC6rqwdlLUkc0yufiTnITvgmPJAN9RzE')
auth.set_access_token("349586645-4e7WmYpjvzKUmsKh3C9pNyv0QzlbVB80nlvR4q02", "qblYvvigttmP5elDFMsIJacO7gOknN794ubMThlyV0pfj")
api = tweepy.API(auth)

class TweetStuff(object):
    @staticmethod
    def getTweets(userId):
        user=api.get_user(userId)
        if user.protected:
            print("User is protected")
            return ""
        timeline=api.user_timeline(screen_name=userId,count=5,tweet_mode="extended")
        tweetTexts=[]
        followerCount=user.followers_count
        followingCount=user.friends_count
        tweetCount=user.statuses_count
        for tweet in timeline:  #taking tweet texts
            if 'retweeted_status' in tweet._json:   #getting full text for retweets
                tweetTexts.append(tweet._json['retweeted_status']['full_text'])
            else:
                tweetTexts.append(tweet.full_text)  #getting full text for self tweets
        tweetDates=[[tweet.created_at]for tweet in timeline]#taking tweet dates
        imageUrls=[]
        for tweet in timeline:#taking image urls of tweets's if it has
            if 'media' in tweet.entities:
                for media in tweet.extended_entities['media']:
                    imageUrls.append(media['media_url'])
            else:
                imageUrls.append("")
        dates=[]
        for t in tweetDates: #string manipulation for better looking  (DD/MM/YYYY)
            for i in t:
                date=str(i).split(" ")[0].split("-")
                dates.append(date[2]+"."+date[1]+"."+date[0])
        profileImage=user.profile_image_url
        informations=[]#Adding all informations to the informations array
        informations.append(tweetTexts)##zerothfirst index tweet texts(contains an array)
        informations.append(dates)##first index dates(contains an array)
        informations.append(tweetCount)##second index (tweet count only an integer)
        informations.append(followingCount)##third index(following count an integer)
        informations.append(followerCount)##fourth index(followerCount an integer)
        informations.append(imageUrls)##fifth index(image Urls an array)
        informations.append(profileImage)
        # for info in informations:
        #     print(info)
        return informations

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json


class InstaStuff(object):
    def parser(username):
        r = requests.get("https://www.instagram.com/"+username+"/?hl=tr")
        source = BeautifulSoup(r.content,"html.parser")
        try:
            pageJS = source.select('script') #selects all the JavaScript on the page
            for i, j in enumerate(pageJS): #Converts pageJS to list of strings so i can calculate length for below. If BS4 has a neater way of doing this, I haven't found it.
                pageJS[i]=str(j)
            script = sorted(pageJS,key=len, reverse=True)[0] #finds the longest bit of JavaScript on the page, which always contains the image data
            scr = json.loads(str(script)[52:-10])

            userInfo = []
            description = []
            likes = []
            urls = []
            user = scr['entry_data']['ProfilePage'][0]['graphql']['user']
            is_private= user['is_private']
            userInfo.append(user['edge_owner_to_timeline_media']['count'])
            userInfo.append(user['edge_followed_by']['count'])
            userInfo.append(user['edge_follow']['count'])

            if  not is_private:
                pics = user['edge_owner_to_timeline_media']['edges']

            for i in range(0,min(5,len(pics))):
                urls.append(pics[i]['node']['display_url'])
                if len(pics[i]['node']['edge_media_to_caption']['edges']) > 0:  #if the pic has no description don't get index out of bounds exception
                    description.append(pics[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
                else:
                    description.append('')
                likes.append(pics[i]['node']['edge_liked_by']['count'])

            retArr = []
            retArr.append(userInfo)
            retArr.append(description)
            retArr.append(likes)
            retArr.append(urls)
            return retArr
        except:
            data = source.find_all('meta', attrs={'property': 'og:description'
                                                })
            text = data[0].get('content').split()

            user = '%s %s %s' % (text[-3], text[-2], text[-1])
            followers = text[0]
            following = text[2]
            posts = text[5]


            exarray =[]
            exarray.append(posts)
            exarray.append(followers)
            exarray.append(following)

            return exarray

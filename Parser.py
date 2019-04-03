from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json


class InstagramParse(object):

    def parser(username):
        r = requests.get("https://www.instagram.com/"+username+"/?hl=tr")
        source = BeautifulSoup(r.content,"html.parser")
        try:
            pageJS = source.select('script')
            for i, j in enumerate(pageJS): 
               pageJS[i]=str(j)
            script = sorted(pageJS,key=len, reverse=True)[0] 
            scr = json.loads(str(script)[52:-10])

            userInfo = []
            description = []
            likes = []
            urls = []
            user = scr['entry_data']['ProfilePage'][0]['graphql']['user']


            
            userInfo.append(user['edge_owner_to_timeline_media']['count'])
            userInfo.append(user['edge_followed_by']['count'])
            userInfo.append(user['edge_follow']['count'])
            pics = user['edge_owner_to_timeline_media']['edges']
    
            for i in range(0,min(5,len(pics))):
                urls.append(pics[i]['node']['display_url'])
                description.append(pics[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
                likes.append(pics[i]['node']['edge_liked_by']['count'])

            retArr = []
            retArr.append(userInfo)
            retArr.append(description)
            retArr.append(likes)
            retArr.append(pics)
            return retArr
        except:
            data = source.find_all('meta', attrs={'property': 'og:description'})
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




import os
from Text_Analyzer import GoogleCloud
from Image_Analyzer import ImageAnalyzer

class Analyze(object):
    @staticmethod
    def isTwitterPublic(output):
        return output != ""
    
    @staticmethod
    def isInstagramPublic(output):
        return len(output) != 3
    
    @staticmethod
    def entityAnalysis(output, type, options_txt, options_img, query=""):
        d = GoogleCloud()
        if type == 0:
            if not Analyze.isTwitterPublic(output):
                return "Protected account."
            else:
                print("Twitter:\nTweets: {}, Following: {}, Followers: {}\n".format(output[2], output[3], output[4]))
        else:
            if not Analyze.isInstagramPublic(output):
                print("Instagram:\nPosts: {}, Followers: {}, Following: {}\n".format(output[0], output[1], output[2]))
                print("User's profile is private.")
                return "Protected account."
            else:
                print("Posts: {}, Followers: {}, Following: {}\n".format(output[0][0], output[0][1], output[0][2]))

        k = 1
        arr_extraInfo = output[1] if type == 0 else output[2]
        arr_txt = output[0] if type == 0 else output[1]
        arr_img = output[5] if type == 0 else output[3]
        d = 0
        for i, j in zip(arr_txt, arr_img):
            print('************************************************************')
            if type == 0:
                print('{} {}\tDate: {}'.format('Tweet', k, arr_extraInfo[d]))
            else:
                print('{} {}\tLikes: {}'.format('Post', k, arr_extraInfo[d]))
            print('************************************************************')
            if options_txt[0] == 1:
                GoogleCloud.classify_text(i)
            if options_txt[2] == 1:
                GoogleCloud.entity_sentiment_analysis(i)
                GoogleCloud.text_sentiment_analysis(i)
            if len(j) !=0:
                ImageAnalyzer.analyze_and_print_from_url(j, options_img[0], options_img[1], options_img[2], options_img[3])
            else:
                print("No image found.\n")
            k = k+1
            d = d+1

        if options_txt[1] == 1:
            k = 1
            arr_txt = output[0] if type == 0 else output[1]
            for i in arr_txt:
                if(type == 0):
                    f = open("resources/tweet{}.txt".format(k), "w", errors='ignore')
                else:
                    f = open("resources/insta{}.txt".format(k), "w", errors='ignore')
                f.write(i)
                f.close()
                k = k+1
            GoogleCloud.index('resources', 'texts.json')
            GoogleCloud.query_category('texts.json', query)
            list = os.listdir('resources')
            for i in list:
                os.remove('resources/{}'.format(i))
import os
from analysis_functions import GoogleCloud


class Analyze(object):
    @staticmethod
    def isTwitterPublic(output):
        return output != ""
    
    @staticmethod
    def isInstagramPublic(output):
        return len(output) != 3
    
    @staticmethod
    def entityAnalysis(output, type, options, query=""):
        d = GoogleCloud()
        if(type == 0):
            if(not Analyze.isTwitterPublic(output)):
                    return "Protected account."
        else:
            if(not Analyze.isInstagramPublic(output)):
                    print("User's profile is private.")
                    return "Protected account."
        if(options[0] == 1):
            if(type == 0):
                k = 1
                arr = output[0]
                for i in arr:
                    print('************************************************************')
                    print('{} {}'.format('Tweet',k))
                    print('************************************************************')
                    GoogleCloud.classify_text(i) 
                    k = k+1
            else:    
                k = 1
                arr = output[1]
                for i in arr:
                    print('************************************************************')
                    print('{} {}'.format('Insta',k))
                    print('************************************************************')
                    GoogleCloud.classify_text(i) 
                    k = k+1
        if(options[1] == 1):
            k = 1
            if(type == 0):
                arr = output[0]
            else:
                arr = output[1]
            for i in arr:
                if(type == 0):
                    f = open("resources/tweet{}.txt".format(k), "w")
                else:
                    f = open("resources/insta{}.txt".format(k), "w")
                f.write(i)
                f.close()
                k = k+1
            GoogleCloud.index('resources', 'texts.json')
            GoogleCloud.query_category('texts.json', query)
            list = os.listdir('resources')
            for i in list:
                os.remove('resources/{}'.format(i))    
        if(options[2] == 1):
            if(type == 0):
                k = 1
                arr = output[0]
                for i in arr:
                    print('************************************************************')
                    print('{} {}'.format('Tweet',k))
                    print('************************************************************')
                    GoogleCloud.entity_sentiment_analysis(i) 
                    GoogleCloud.text_sentiment_analysis(i)
                    k = k+1
            else:    
                k = 1
                arr = output[1]
                for i in arr:
                    print('************************************************************')
                    print('{} {}'.format('Insta',k))
                    print('************************************************************')
                    GoogleCloud.entity_sentiment_analysis(i) 
                    GoogleCloud.text_sentiment_analysis(i)
                    k = k+1
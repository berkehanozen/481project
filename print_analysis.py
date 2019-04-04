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
            if not Analyze.isInstagramPublic(output):
                    print("User's profile is private.")
                    return "Protected account."

        k = 1
        arr_txt = output[0] if type == 0 else output[1]
        arr_img = output[5] if type == 0 else output[3]
        for i, j in zip(arr_txt, arr_img):
            print('************************************************************')
            if type == 0:
                print('{} {}'.format('Tweet', k))
            else:
                print('{} {}'.format('Post', k))
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
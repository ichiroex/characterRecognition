#coding: utf-8
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import json
import time 
import urllib
import re
import sys

#画像データを投げて、画像のIDをjson形式で取得 (情景画像認識要求)
def getImageID(fname):
    register_openers()
    
    APIKEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    url = 'https://api.apigw.smt.docomo.ne.jp/characterRecognition/v1/document?APIKEY=' + APIKEY
    
    f = open(fname, 'r')

    datagen, headers = multipart_encode({"image": f, 'lang': 'jpn'})
    request = urllib2.Request(url,datagen, headers)
    response = urllib2.urlopen(request)
    
    res_dat = response.read()
    return json.loads(res_dat)['job']['@id'] #画像のIDを返す

#取得したjsonから単語だけを取り出す。
def makeWordList(result):
    
    word_list = []
    count  = int(result['lines']['@count'])

    for i in range(count):
        word = result['lines']['line'][i]['@text']
        word_list.append(word)

    return word_list

#情景画像認識結果取得
def getWordList(img_id):

    register_openers()
    APIKEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    url = 'https://api.apigw.smt.docomo.ne.jp/characterRecognition/v1/document/' + img_id + '?APIKEY=' + APIKEY
    
    request = urllib2.Request(url)
    
    recog_result = {}
    for i in range(5):
        response = urllib2.urlopen(request)
        res_dat = response.read()
        
        recog_result = json.loads(res_dat)
        
        status = recog_result['job']['@status']
        
        if status == 'queue':
            print '受付中...'
        elif status == 'process':
            print '認識処理中...'
        elif status == 'success':
            print '認識成功' #, recog_result
            word_list = makeWordList(recog_result)
            #print json.dumps(recog_result, indent=2) #jsonを表示する
            return word_list
        elif status == 'failure':
            print '認識失敗'
            return None

        time.sleep(3) #ちょっと待つ



if __name__ == '__main__':

    img_id = getImageID(sys.argv[1])

    
    word_list = getWordList(img_id)
    
    #認識した文字列を表示
    for word in word_list:
        print word


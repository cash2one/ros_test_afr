#!/usr/bin/env python
#coding=utf-8

import json
import urllib
import urllib2
import ConfigParser
import subprocess
from baidu_nlu.srv import *
import rospy

'''
Baidu TTS Service need to register in http://yuyin.baidu.com
create your application, after that you will have your cuid,apikey,secretkey
all the information write in the nlu.cfg file like this:

[baidu]
CUID = your cuid
API_KEY = your application key
SECRET_KEY = your secret key


'''


def get_config():
    config = ConfigParser.ConfigParser()
    config.read('nlu.cfg')
    return config.get('baidu','CUID'),config.get('baidu','API_KEY'),config.get('baidu','SECRET_KEY')

def get_baidu_auth():

    _,API_KEY,SECRET_KEY = get_config()
    auth_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API_KEY+'&client_secret='+SECRET_KEY
    res = json.loads(download(auth_url))
    return res['access_token']


def download(link,data=None,headers={}):
    try:
        req = urllib2.Request(link,data,headers)
        response = urllib2.urlopen(req,None,15)
        res = response.read()
    except:
        return None

    return res


def tts_test(msg):

    text = urllib.quote(msg)
    tts_url = 'http://tsn.baidu.com/text2audio?tex='+ text +'&lan=zh&cuid=6405099&ctp=1&tok=%s'% access_token
    res = download(tts_url)
    fw = open('read.mp3','wb')
    fw.write(res)
    fw.close()
    subprocess.Popen(['mplayer','read.mp3'])
    return msg

def handle_tts(req):
    print 'request is ',req.natural_language_json

    return TTSResponse(tts_test(req.natural_language_json))

def tts_server():
    rospy.init_node('tts_server')
    s = rospy.Service('tts',TTS,handle_tts)
    print 'ready to read the sentence'
    rospy.spin()

if __name__ == '__main__':
    access_token = get_baidu_auth()
    tts_server()

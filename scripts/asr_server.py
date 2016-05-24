#!/usr/bin/env python
#coding=utf-8

import json
import base64
import urllib
import urllib2
import ConfigParser
import subprocess
from baidu_nlu.srv import *
import rospy

'''
Baidu ASR Service need to register in http://yuyin.baidu.com
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

    CUID,API_KEY,SECRET_KEY = get_config()
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


def asr_test(msg):
    CUID,API_KEY,SECRET_KEY = get_config()
    subprocess.call('''arecord -r 16000 -f S16_LE -D 'plughw:1,0' -d 3 > in.wav''',shell=True)
    with open('in.wav','rb') as fr:
        content = fr.read()
        base_data = base64.b64encode(content)
    
    params = {}
    params['format'] = 'wav'
    params['rate'] = 16000
    params['channel'] = 1
    params['token'] = access_token
    params['cuid'] = CUID
    params['len'] = len(content)
    params['speech'] = base_data

    data = json.dumps(params)
    headers = {
        "Content-Length":len(data),
        "Content-Type":"application/json; charset=utf-8",
        }
    url ='http://vop.baidu.com/server_api'
    res = json.loads(download(url,data,headers))


    return res['result'][0].encode('utf-8')

def handle_asr(req):
    print 'request is ',req.controller_json

    return ASRResponse(asr_test(req.controller_json))

def asr_server():
    rospy.init_node('asr_server')
    s = rospy.Service('asr',ASR,handle_asr)
    print 'ready to listen'
    rospy.spin()

if __name__ == '__main__':
    access_token = get_baidu_auth()
    asr_server()

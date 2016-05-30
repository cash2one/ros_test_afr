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

from facepp import API,File

'''
FacePlusPlus Service need to register in http://www.faceplusplus.com
create your application, after that you will have your apikey,secretkey
all the information write in the nlu.cfg file like this:

[faceplusplus]

API_KEY = your application key
API_SECRET = your secret key


'''


def get_config():
    config = ConfigParser.ConfigParser()
    config.read('nlu.cfg')
    return config.get('faceplusplus','SERVER'),config.get('faceplusplus','API_KEY'),config.get('faceplusplus','API_SECRET')



def afr_test(msg):
    subprocess.call('raspistill -o face.jpg -t 300 -w 480 -h 360 ',shell=True)
    result = api.recognition.recognize(img = File('face.jpg'), group_name = 'ry_robot_001')
    #print 'result',result
    if result['face']:
        return result['face'][0]['candidate'][0]['person_name']
    else:
        return 'no person'

def handle_afr(req):
    print 'request is ',req.controller_json

    return AFRResponse(afr_test(req.controller_json))

def afr_server():
    rospy.init_node('afr_server')
    s = rospy.Service('afr',AFR,handle_afr)
    print 'ready to see your face'
    rospy.spin()

if __name__ == '__main__':
    _,API_KEY,API_SECRET = get_config()
    api = API(API_KEY,API_SECRET)
    afr_server()

#!/usr/bin/env python
#coding=utf-8

import urllib2
import ConfigParser

from baidu_nlu.srv import *
import rospy



def get_config():
    config = ConfigParser.ConfigParser()
    config.read('nlu.cfg')
    return config.get('tuling','API_KEY')

def chat_test(msg):

    url = 'http://www.tuling123.com/openapi/api?key=%s&info=%s'%(API_KEY,msg)

    response = urllib2.urlopen(url).read()

    return response

def handle_chat(req):
    print 'request is ',req.natural_language_json

    return CHATResponse(chat_test(req.natural_language_json))

def chat_server():
    rospy.init_node('chat_server')
    s = rospy.Service('chat',CHAT,handle_chat)
    print 'ready to chat with U'
    rospy.spin()

if __name__ == '__main__':
    API_KEY = get_config()
    chat_server()

#!/usr/bin/env python
#coding=utf-8

import urllib2

from baidu_nlu.srv import *
import rospy






def tts_test(msg):

    domainIds = ','.join([str(x) for x in xrange(1,30)])
    url = 'http://yuyin.baidu.com/nlp/analysisPreview?domainIds=%s&query=%s'%(domainIds,msg)
    response = urllib2.urlopen(url).read()

    return response

def handle_tts(req):
    print 'request is ',req.natural_language_json

    return TTSResponse(tts_test(req.natural_language_json))

def tts_server():
    rospy.init_node('tts_server')
    s = rospy.Service('tts',TTS,handle_tts)
    print 'ready to read the sentence'
    rospy.spin()

if __name__ == '__main__':
    tts_server()

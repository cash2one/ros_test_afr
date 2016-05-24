#!/usr/bin/env python
#coding=utf-8

import urllib2

from baidu_nlu.srv import *
import rospy


def nlu_test(msg):

    domainIds = ','.join([str(x) for x in xrange(1,30)])
    url = 'http://yuyin.baidu.com/nlp/analysisPreview?domainIds=%s&query=%s'%(domainIds,msg)
    response = urllib2.urlopen(url).read()

    return response

def handle_nlu(req):
    print 'request is ',req.natural_language_json

    return NLUResponse(nlu_test(req.natural_language_json))

def nlu_server():
    rospy.init_node('nlu_server')
    s = rospy.Service('nlu',NLU,handle_nlu)
    print 'ready to parse the sentence'
    rospy.spin()

if __name__ == '__main__':
    nlu_server()

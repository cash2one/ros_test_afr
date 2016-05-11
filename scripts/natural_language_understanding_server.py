#!/usr/bin/env python

from baidu_nlu.srv import *
import rospy


def handle_nlu(req):
    print 'request is ',req.natural_language_json
    return NLUResponse(req.natural_language_json+'===')

def nlu_server():
    rospy.init_node('nlu_server')
    s = rospy.Service('nlu',NLU,handle_nlu)
    print 'ready to parse the sentence'
    rospy.spin()

if __name__ == '__main__':
    nlu_server()


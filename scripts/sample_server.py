#!/usr/bin/env python
#coding=utf-8

import json
import base64
import time


from baidu_nlu.srv import *
import rospy


def led():

    rospy.wait_for_service('led')
    try:
        led_s = rospy.ServiceProxy('led',LED)
        res = led_s('')
    except rospy.ServiceException,e:
        print 'led call failed:%s'%e

def tts(content):
    rospy.wait_for_service('tts')
    try:
        tts_s = rospy.ServiceProxy('tts',TTS)
        res = tts_s(content)
    except rospy.ServiceException,e:
        print 'tts call failed:%s'%e

def afr():

    rospy.wait_for_service('afr')
    try:
        afr_s = rospy.ServiceProxy('afr',AFR)
        res = afr_s('')
        tts('你是%s'%res.processing_result_json)
    except rospy.ServiceException,e:
        print 'afr call failed:%s'%e
    
def asr():
    
    rospy.wait_for_service('asr')
    try:
        asr_s = rospy.ServiceProxy('asr',ASR)
        res = asr_s('')
        chat(res.processing_result_json)
    except rospy.ServiceException,e:
        print 'asr call failed:%s'%e

def nlu():
    pass

def chat(content):
    
    rospy.wait_for_service('chat')
    try:
        chat_s = rospy.ServiceProxy('chat',CHAT)
        res = chat_s(content)
        tts(res.processing_result_json)
    except rospy.ServiceException,e:
        print 'chat call failed:%s'%e


def sample_test(msg):
    
    if msg == 'afr':
        tts('请将您的脸对准摄像头')
        afr()    
    elif msg == 'chat':
        tts('我们开始聊天吧')
        asr()
    
    elif msg == 'nlu':
        print msg    
    elif msg == 'led':
        tts('下面进行10秒钟的灯光演示')
        led()    


    return msg
    
def handle_sample(req):
    print 'request is ',req.controller_json

    return SAMPLEResponse(sample_test(req.controller_json))

def sample_server():
    rospy.init_node('sample_server')
    s = rospy.Service('sample',SAMPLE,handle_sample)
    print 'ready to try'
    rospy.spin()

if __name__ == '__main__':
    sample_server()

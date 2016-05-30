#!/usr/bin/env python
#coding=utf-8

import json
import base64
import time

import RPi.GPIO as GPIO

from baidu_nlu.srv import *
import rospy


def led_test(msg):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)


    for i in xrange(1,10):
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(15,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        GPIO.output(15,GPIO.LOW)
        time.sleep(0.5)

    GPIO.cleanup()

    return msg
    
def handle_led(req):
    print 'request is ',req.controller_json

    return LEDResponse(led_test(req.controller_json))

def led_server():
    rospy.init_node('led_server')
    s = rospy.Service('led',LED,handle_led)
    print 'ready to switch led'
    rospy.spin()

if __name__ == '__main__':
    led_server()

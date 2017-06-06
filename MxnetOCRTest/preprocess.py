#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 22:24:14 2017

@author: zhouhang
"""

import os,string
import cv2
fileList = os.listdir('./sub')
for i in fileList:
    if os.path.splitext(i)[1][1:] == 'png':
        print i
        img = cv2.imread('./sub/'+i)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('./sub/'+os.path.splitext(i)[0]+'.jpg',img)
        os.remove('./sub/'+i)
        
sampleCount = {}
for i in fileList:
    if os.path.splitext(i)[1][1:] == 'jpg':
        number = string.atoi(os.path.splitext(i)[0][0:2])
        if sampleCount.has_key(number):
            sampleCount[number]+=1
        else:
            sampleCount[number]=1

print sampleCount
        
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 23:08:08 2017

@author: zhouhang
"""

import mxnet as mx
import numpy as np
from matplotlib import pyplot as plt
import cv2, os, string
import logging 
xSz = 20
ySz = 20
readDir = '/Users/zhouhang/Documents/MyProject/Github/MachineLearning/MachineLearning/mxnet/test-zhousl/'
#readDir = '/Users/zhouhang/Documents/MyProject/Github/MachineLearning/MachineLearning/mxnet/sub/'
fileList = os.listdir(readDir)
imgData = np.zeros((len(fileList),1,xSz,ySz))
preData = np.zeros((1,1,xSz,ySz))
model = mx.model.FeedForward
mod = model.load('ocr1_',100,ctx=mx.cpu())
offset = 73
id=0
for i in fileList:
    if os.path.splitext(i)[1][1:] == 'png':
        tmp = cv2.imread(readDir+i,cv2.IMREAD_UNCHANGED)
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        tmp = cv2.resize(tmp,(xSz,ySz))
        imgData[id,0, :,:] = tmp.copy()
        label = string.atoi(i[0:2])
        preData[0,0,:,:] =  imgData[id,0, :,:]
        resList = mod.predict(preData)
        res1 = resList.argmax()+offset
        resList[0,resList.argmax()]=0.0
        res2 = resList.argmax()+offset
        print "predict:",res1, ' 2nd:',res2," label:",i
        id+=1
        
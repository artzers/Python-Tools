#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 11:57:21 2017

@author: zhouhang
"""
import cv2,mxnet as mx
import matplotlib
from matplotlib import pyplot as plt
offset = 73
xSz = 20
ySz = 20
preData = np.zeros((1,1,xSz,ySz))
model = mx.model.FeedForward
mod = model.load('ocr1_',100,ctx=mx.cpu())
tmp=cv2.imread('final1.png')
tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
id = 1
ylen = 65
for y in xrange(0,tmp.shape[0], ylen):
    sub = tmp[y:y+ylen,:]
    sub = cv2.resize(sub,(xSz,ySz))
    fig = plt.figure(id)
    imshow(sub,cmap='gray')
    preData[0,0,:,:] =  sub
    res = mod.predict(preData).argmax()+offset
    print id," predict:",res
    id +=1
    

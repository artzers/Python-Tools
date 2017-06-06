#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 10:55:59 2017

@author: zhouhang
"""

import mxnet as mx
import numpy as np
from matplotlib import pyplot as plt
import cv2, os, string
import logging  

#readDir = '/Users/zhouhang/Documents/MyProject/Github/MachineLearning/MachineLearning/mxnet/preprocess-zhousl/'
#writeSubDir = '/Users/zhouhang/Documents/MyProject/Github/MachineLearning/MachineLearning/mxnet/preprocess-zhousl/sub/'
#fileList=[]
#tmpList = os.listdir(readDir)
#for i in tmpList:
#    if os.path.splitext(i)[1][1:] == 'jpg':
#            fileList.append(i)
#            
#xStep = 160
#yStep = 170
#for i in fileList:
#    img = cv2.imread(i,cv2.IMREAD_UNCHANGED)
#    prefix = os.path.splitext(i)[0]
#    for x in xrange(0, 770, 2*xStep):
#        for y in xrange(0, 2500, yStep):
#            subimg = img[y:y+yStep, x:x+xStep]
#            cv2.imwrite(writeSubDir+prefix+'%d_%d.jpg'%(x,y), subimg)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #_,img = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
#plt.imshow(img,cmap ='gray')

#cv2.imwrite('bin.jpg',img)

#img = cv2.imread('bin.tif',cv2.IMREAD_UNCHANGED)
#140 150
#xStep = 160
#yStep = 170
#for x in xrange(0, 770, 2*xStep):
#    for y in xrange(0, 2500, yStep):
#        subimg = img[y:y+yStep, x:x+xStep]
#        cv2.imwrite('sub/%d_%d.jpg'%(x,y), subimg)

dirName = '/Users/zhouhang/Documents/MyProject/Github/MachineLearning/MachineLearning/mxnet/sub/'
tmpList = os.listdir(dirName)
       
fileList=[]
for i in tmpList:
    if os.path.splitext(i)[1][1:] == 'jpg':
            fileList.append(i)

xSz = 20
ySz = 20
#imgData = np.zeros((len(fileList),1, 170,160),np.uint8)
imgData = np.zeros((len(fileList),1, xSz,ySz),np.uint8)
label= []
for i in xrange(0, len(fileList)):
    #print i
    tmp = cv2.imread(dirName+fileList[i],cv2.IMREAD_UNCHANGED)
    imgData[i,0, :,:] = cv2.resize(tmp,(xSz,ySz))#(160,170)
    label.append(string.atoi(fileList[i][0:2]))
    #imgData[i,:,:]= cv2.imread(fileList[i],cv2.IMREAD_UNCHANGED)
label = np.array(label)
offset = label.min()
outputNum = label.max() - offset + 1
print "outPutNum:",outputNum
print 'offset:',offset
label -= offset
    
X_ = mx.sym.Variable('data')
y_ = mx.sym.Variable('softmax_label')

conv1 = mx.symbol.Convolution(name = 'conv1', data = X_, kernel = (3,3),pad = (1,1), num_filter = 4)
relu1= mx.symbol.Activation(name = 'act1', data = conv1, act_type = 'relu')
flat = mx.symbol.Flatten(name = 'flat1', data = relu1)
drop = mx.symbol.Dropout(name='dropout',data = flat, p=0.1)
fc1 = mx.symbol.FullyConnected(name='fc1',data = drop, num_hidden=outputNum)
loss = mx.symbol.SoftmaxOutput(name = 'softmax_loss',data = fc1, label=y_)

train_iter=mx.io.NDArrayIter(imgData, label = label,batch_size=20,shuffle=True, last_batch_handle='roll_over')

eval_iter=mx.io.NDArrayIter(imgData, label = label,batch_size=20,shuffle=True, last_batch_handle='roll_over')


def mycall(epoch, symbol, arg_params, aux_states):
    print 'epoch:%d'%epoch
    
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

model = mx.model.FeedForward(
    ctx                = mx.cpu(),
    symbol             = loss,
    num_epoch          = 100,
    learning_rate      = 0.001,
    momentum           = 0.9,
    wd                 = 0.0001)
model.fit(
    X                  = train_iter,
    eval_data          = eval_iter,
    eval_metric='acc',
    epoch_end_callback = None)#mycall
model.save('ocr1_')

test = np.zeros((1,1,20,20))
test[0,0,:,:] = imgData[34,0,:,:].copy()
res = model.predict(test).argmax()+offset
print res
print label[34]+offset
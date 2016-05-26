# -*- coding:gb2312 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os, hashlib,shutil,codecs
import numpy as np
from collections import defaultdict
from collections import OrderedDict

def VisitDir(arg,dirname,names):
        for filespath in names:
                name = os.path.join(dirname,filespath)
                if not os.path.isdir(name):
                        fileList.append(name)
#if __name__=="__main__":
sep = os.sep
dirName = raw_input("Please input dir name.")#u"/Users/zhouhang/Pictures/ͼƬ"#
dirPath = unicode(dirName,"utf8") + sep
if not os.path.exists(dirPath):
        print "%s is invalid!"%(dirPath)
        exit(0)
fileList=[]
os.path.walk(dirPath, VisitDir, fileList)
print "complete"
md5list=defaultdict(list)
tenPercent = len(fileList) / 10
count = 0
for i in fileList:
        count += 1
        md5file=open(i,"rb")
        md5=hashlib.md5(md5file.read()).hexdigest()
        md5file.close()
        md5list[md5].append(i)
        if np.mod(count, tenPercent) == 0:
                print "%d percent md5 complete"%(count * 100 / len(fileList))
print "md5 complete"
#trashDir = dirName + sep + "tmpTrash/"
repeatFileName = dirName + sep + "repeatFileList.txt"
tenPercent = len(md5list) / 10
count = 0
with codecs.open(repeatFileName, 'w') as f:
    for i in md5list:
            count += 1
            if np.mod(count, tenPercent) == 0:
                print "%d percent md5 complete" % (count * 100 / len(fileList))
            if len(md5list[i]) > 1:
                    f.writelines("---------------\n")
                    #if not os.path.exists(trashDir):
                    #        os.mkdir(trashDir)
                    ind = 1
                    for j in md5list[i]:
                            print ind,":",j
                            ind += 1
                            f.write(j)
                            f.write("\n")
                    # flag = int(raw_input("what file will you want to remove?"))
                    # if flag not in  range(1,len(md5list[i])+1):
                    #         continue
                    # else:
                    #         rfile = md5list[i][flag-1]
                    #         print "remove ", rfile," to %s"%(trashDir)
                    #         try:
                    #                 shutil.move(rfile, trashDir)
                    #         except Exception, e:
                    #                 print Exception,":",e


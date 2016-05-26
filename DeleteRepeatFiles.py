# coding=gbk
import os, hashlib,shutil
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
dirPath = dirName + sep
if not os.path.exists(dirPath):
        print "the dir is invalid!"
        exit(0)
fileList=[]
os.path.walk(dirName, VisitDir, fileList)
print "complete"
md5list=defaultdict(list)
for i in fileList:
        md5file=open(i,"rb")
        md5=hashlib.md5(md5file.read()).hexdigest()
        md5file.close()
        md5list[md5].append(i)
trashDir = dirName + sep + "tmpTrash/"
for i in md5list:
        if len(md5list[i]) > 1:
                if not os.path.exists(trashDir):
                        os.mkdir(trashDir)
                ind = 1
                for j in md5list[i]:
                        print ind,":",j
                        ind += 1
                flag = int(raw_input("what file will you want to remove?"))
                if flag not in  range(1,len(md5list[i])+1):
                        continue
                else:
                        rfile = md5list[i][flag-1]
                        print "remove ", rfile," to %s"%(trashDir)
                        try:
                                shutil.move(rfile, trashDir)
                        except Exception, e:
                                print Exception,":",e


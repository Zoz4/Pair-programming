import os
import requests
from PIL import Image
import cv2
import base64
import json
from trainTools import *

# 将900*900的图片裁剪为9块(image：要裁剪的图片；filePath：裁剪的图片保存路径)
def cutImage(image,filePath):
    for y in range(3):
        for x in range(3):
            cropImage = image[y*300:(y+1)*300,x*300:(x+1)*300]
            grayImage = cv2.cvtColor(cropImage,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(filePath+'/'+str(y*3+x+1)+'.jpg',grayImage,[cv2.IMWRITE_JPEG_QUALITY,100])
# 将给定路径下的文件夹的900*900图片裁剪为9块
def cutSourceImage(filePath):
    imagenames = os.listdir(filePath)
    for imagename in imagenames:
        if os.path.isdir(filePath+'/'+imagename):
            continue
        dirname = imagename.replace('.jpg','')
        image = cv2.imread(filePath+'/'+imagename)
        if not os.path.exists(filePath+'/'+dirname):
            os.mkdir(filePath+'/'+dirname)
        cutImage(image,filePath+'/'+dirname)
        os.remove(filePath+'/'+imagename)


def isWhiteImage(image):
    ls = np.bincount(image.ravel(),minlength=256)
    if(ls[255] > 210000):
        return True
    else:
        return False
if __name__ == '__main__':
    print('ctools.py')
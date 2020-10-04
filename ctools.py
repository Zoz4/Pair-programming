import os
import requests
from PIL import Image
import cv2
import base64
import json

def getProblemJsonFile(url):
    r = requests.get(url)
    return r.json()
# 读取json文件
def readAnswerJsonFile(filePath):
    with open(filePath,'r') as jsonFile:
        dict = json.load(jsonFile)
    return dict
# 把base64编码的图片保存到指定路径
def writeImage(filePath, base64Image):
    image = base64.b64decode(base64Image)
    with open(filePath,'wb') as fileObject:
        fileObject.write(image)
# 将900*900的图片裁剪为9块
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
# 比较两张图片的相似性
def compareImage(image1, image2):
    return 


js = getProblemJsonFile('http://47.102.118.1:8089/api/problem?stuid=031802230')
#print(type(js))
#dict = readAnswerJsonFile('./test.json')
writeImage('./2.jpg',js['img'])
image = cv2.imread('2.jpg')
cutImage(image, './2')


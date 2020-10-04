
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
            box = (x*300,y*300,(x+1)*300,(y+1)*300)
            cropImage = image.crop(box)
            cropImage.save(filePath+'/'+str(y*3+x+1)+'.jpg')
# 将给定路径下的文件夹的900*900图片裁剪为9块
def cutSourceImage(filePath):
    imagenames = os.listdir(filePath)
    for imagename in imagenames:
        if os.path.isdir(filePath+'/'+imagename):
            continue
        dirname = imagename.replace('.jpg','')
        image = Image.open(filePath+'/'+imagename)
        if not os.path.exists(filePath+'/'+dirname):
            os.mkdir(filePath+'/'+dirname)
        cutImage(image,filePath+'/'+dirname)
# 比较两张图片的相似性
def compareImage(image1, image2):
    return 


#js = getProblemJsonFile('http://47.102.118.1:8089/api/problem?stuid=031802230')
#print(type(js))
#dict = readAnswerJsonFile('./test.json')
#writeImage('./1.jpg',dict['img'])

image1 = Image.open('./target/1.jpg')
l1 = image1.convert(mode='1').histogram()
print(len(l1))
print(l1)
image2 = Image.open('./source/A_/7.jpg')
l2 = image2.convert(mode='1').histogram()
print(len(l2))
print(l2)
if l1 == l2:
    print("Yes")

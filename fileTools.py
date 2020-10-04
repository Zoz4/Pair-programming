import os
import requests
import cv2
import base64
import json
from trainTools import *


# HTTP GET
def getProblemJsonFile(url):
    r = requests.get(url)
    return r.json()

# 读取json文件
def readJsonFile(filePath):
    with open(filePath,'r') as jsonFile:
        dict = json.load(jsonFile)
    return dict
# 把字典文件保存为json文件
def saveDictFile(dict,filePath):
    with open(filePath,'w') as jsonFile:
        json.dump(dict, jsonFile)

# 把base64编码的图片保存到指定路径
def writeBase64Image(filePath, base64Image):
    image = base64.b64decode(base64Image)
    with open(filePath,'wb') as fileObject:
        fileObject.write(image)

# 找到原图片中黑色图片的编号
def findSourceBlackPictureNo(filePath):
    BlackPictureNo = {}
    fileNames = os.listdir(filePath)
    fileNames.sort()
    for fileName in fileNames:
        for i in range(1,10):
            img = cv2.imread(filePath+'/'+fileName+'/'+str(i)+'.jpg')
            corners = getCorners(img)
            if(corners.size <= 1):
                if fileName[0] not in BlackPictureNo.keys():
                    BlackPictureNo[fileName[0]] = str(i)
                else:
                    BlackPictureNo[fileName[0]] += str(i)
#    for key,value in BlackPictureNo.items():
#        print(key+' : '+ value)
    return BlackPictureNo

if __name__ == '__main__':
    print('fileTools.py')

#    with np.load('./record/knnTrainData.npz') as data:
#        print(data.files)
#        trainData = data['trainData']
#        responses = data['responses']   
 #   charDict = getCharDict('./source')
#    saveDictFile(charDict,'./record/charDict.json')
#   charDict = readJsonFile('./record/charDict.json')
#    noDict = {}
#    for key,value in charDict.items():
#        noDict[value] = key
#    saveDictFile(noDict,'./record/noDict.json')
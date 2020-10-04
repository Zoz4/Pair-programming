import cv2
import numpy as np
import os
# 得到一张图片的特征值
def getCorners(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
    corners = np.float32(corners)
    return corners
# 得到一张图片的训练数据（特征值的列表）
def getImageTrainData(image):
    corners = getCorners(image)
    TrainData = np.empty((0,2),np.float32)
    if (corners.size > 1):
        for j in corners:
            TrainData = np.append(TrainData,j,axis=0)
    return TrainData
# 得到图片名称（A，a，B....）与相应标记的映射
def getCharDict(filePath):
    dirNames = os.listdir(filePath)
    dirNames.sort()
    i = 1.0
    charDict = {}
    for dirName in dirNames:
        for j in range(1,10):
            charDict[dirName[0]+str(j)] = i
            i = i+1.0
    return charDict

def getKNNTrainData(filePath):
    charDict = getCharDict(filePath)
    dirNames = os.listdir(filePath)
    trainData = np.empty((0,2),np.float32)
    responses = np.empty((0,1),np.float32)
    for dirName in dirNames:
        for i in range(1,10):
            image = cv2.imread(filePath+'/'+dirName+'/'+str(i)+'.jpg')
            td = getImageTrainData(image)
            tr = np.full((len(td),1),np.float32(charDict[dirName[0]+str(i)]))
            trainData = np.append(trainData,td,axis=0)
            responses = np.append(responses,tr,axis=0)
    print(trainData.shape)
    print(responses.shape)
    knn = cv2.ml.KNearest_create()
    knn.train(trainData,cv2.ml.ROW_SAMPLE,responses)
    timg = cv2.imread('./2/1.jpg')
    test = getImageTrainData(timg)
    ret,result,neighours,dist = knn.findNearest(test,k=2)
    print(ret)
    for key in charDict.keys():
        if (charDict[key] == ret):
            print(key)
            break


filePath = './source'
#print(getCharDict(filePath))
startTrain(filePath)



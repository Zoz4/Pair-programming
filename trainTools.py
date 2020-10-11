import cv2
import numpy as np
import os

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

# 得到一张图片的特征值
def getCorners(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
    corners = np.float32(corners)
    return corners
# 得到一张图片的训练数据（ 特征值的 ndarray.shape = (n,2) )
def getImageTrainData(image):
    corners = getCorners(image)
    TrainData = np.empty((0,2),np.float32)
    if (corners.size > 1):
        for j in corners:
            TrainData = np.append(TrainData,j,axis=0)
    return TrainData
# 得到KNN的训练数据，将其保存到filePath中的
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
    np.savez('./record/knnTrainData.npz',trainData = trainData, responses = responses)

def getClosestResult(results):
    count = {}
    for result in results:
        if result[0] not in count.keys():
            count[result[0]] = 1
        else:
            count[result[0]] += 1
    closestResult = 0.0
    max = 0
    for key,value in count.items():
        if (count[key] > max):
            max = count[key]
            closestResult = key
    return closestResult

if __name__ == '__main__':
    print('trainTools.py')
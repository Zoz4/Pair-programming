import cv2, base64, json, os, requests
import numpy as np
from fileTools import *
from trainTools import *
from imgTools import *
from eightPuzzle import *

if __name__ == '__main__':
    probUrl = 'http://47.102.118.1:8089/api/problem'
    probParams = {'stuid':'031802230'}
    ansUrl = 'http://47.102.118.1:8089/api/answer'
    ansParams = {
        'uuid':'',
        'answer':{
            'operations':'',
            'swap':[]
        }
    }

    # 得到问题图片，裁剪保存到./target
    problem = requests.get(probUrl,params=probParams)
    problemJson = problem.json()
    writeBase64Image('./problem.jpg',problemJson['img'])
    problemImage = cv2.imread('./problem.jpg')
    cutImage(problemImage,'./target')

    # 载入分割的原字符图片到responses（trainLabels）的映射
    # 载入responses（trainLabels）到分割的原字符图片的映射
    charDict = readJsonFile('./record/charDict.json')
    noDict = readJsonFile('./record/noDict.json')
    # 载入训练数据并训练
    with np.load('./record/knnTrainData.npz') as data:
        trainData = data['trainData']
        responses = data['responses']
    knn = cv2.ml.KNearest_create()
    knn.train(trainData,cv2.ml.ROW_SAMPLE,responses)
    

    findWhiteImageflag = 0
    problemWhiteImageNo = -1
    problemBlackImageNo = []
    match = {}
    for i in range(1,10):
        image = cv2.imread('./target'+'/'+str(i)+'.jpg')
        corners = getImageTrainData(image)
        # 没有特征点（纯白或纯黑图片）
        if(corners.size < 1):
            if(isWhiteImage(image)):
                problemWhilteImageNo = i
            else:
                problemBlackImageNo.append(i)
        else:
            
            ret,results,neighbours,dist = knn.findNearest(corners,k=1)
            result = getClosestResult(results)
            match[i] = noDict[str(result)]
#    for key,value in match.items():
#        print(str(key) + '   = ' + value)





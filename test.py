import cv2, base64, json, os, requests
import numpy as np
from fileTools import *
from trainTools import *
from imgTools import *
from eightPuzzle import *

with np.load('./record/knnTrainData.npz') as data:
        print(data.files)
        trainData = data['trainData']
        responses = data['responses']
knn = cv2.ml.KNearest_create()
knn.train(trainData,cv2.ml.ROW_SAMPLE,responses)

charDict = readJsonFile('./record/charDict.json')
noDict = readJsonFile('./record/noDict.json')

fileNames = os.listdir('./source')
fileNames.sort()
j = 1
for fileName in fileNames:
    for i in range(1,10):
        img = cv2.imread('./source'+'/'+fileName+'/'+str(i)+'.jpg')
        test = getImageTrainData(img)
        if(test.size > 1):
            ret,results,neighbours,dist = knn.findNearest(test,k=1)
            result = getClosestResult(results)
            #print('p:   ' + fileName[0]+str(i) +'  m:   '+noDict[str(result)])
            if((fileName[0]+str(i)) != noDict[str(result)]):
                print('p:   ' + fileName[0]+str(i) +'  m:   '+noDict[str(result)])
            else:
                print(j)
                j += 1
            



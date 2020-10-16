import cv2, base64, json, os, requests
import numpy as np
from fileTools import *
from trainTools import *
from imgTools import *
from eightPuzzle import *
from interface import *

teamInformation = {"teamid":40,"token":"4ffaa044-e49a-4b85-b667-39076c7f9e90"}
headers = {'content-type': "application/json"}
charDict = readJsonFile('./record/charDict.json')
noDict = readJsonFile('./record/noDict.json')
blackPictureNo = readJsonFile('./record/BlackPictureNo.json')
with np.load('./record/knnTrainData.npz') as data:
    trainData = data['trainData']
    responses = data['responses']
knn = cv2.ml.KNearest_create()
knn.train(trainData,cv2.ml.ROW_SAMPLE,responses)

def solveProblem(challenge_uuid):
    startUrl = 'http://47.102.118.1:8089/api/challenge/start/' + challenge_uuid
    submitUrl = 'http://47.102.118.1:8089/api/challenge/submit'
    submitData = {
       "uuid": "",
       "teamid": teamInformation["teamid"],
       "token": teamInformation["token"],
       "answer": {
       "operations": "",
       "swap": []
       }
    }
    problem = requests.post(startUrl,data=json.dumps(teamInformation),headers = headers)
    problemJson = problem.json()
    writeBase64Image('./problem.jpg',problemJson['data']['img'])
    problemImage = cv2.imread('./problem.jpg')
    cutImage(problemImage,'./target')

    problemWhiteImageNo = -1
    problemBlackImageNo = []
    match = {}
    for i in range(1,10):
        image = cv2.imread('./target'+'/'+str(i)+'.jpg')
        corners = getImageTrainData(image)
        if(corners.size < 1):
            if(isWhiteImage(image)):
                problemWhiteImageNo = i
            else:
                problemBlackImageNo.append(i)
        else:
            ret,results,neighbours,dist = knn.findNearest(corners,k=1)
            result = getClosestResult(results)
            match[i] = noDict[str(result)]

    cur = np.full((3,3),0)
    goalChar = ''
    matchNo = []
    notMatchNo = []
    location = ([-1,-1],[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2])

    for value in match.values():
        goalChar += value[0]
        matchNo.append(int(value[1]))
    for i in range(1,10):
        if i not in matchNo:
            notMatchNo.append(i)
    notMatchCnt = len(notMatchNo)

    for i in range(1,10):
        if i not in match.keys():
            continue
        x,y = location[i]
        cur[x,y] = int(match[i][1])
    wx,wy = location[problemWhiteImageNo]
    if(goalChar[0] != 'F'):
        if(notMatchCnt == 1):
            whiteNo = notMatchNo[0]
            goal = getGoal(whiteNo)
            e = eightDigitalCode(wx,wy,cur,goal)
        elif(notMatchCnt == 2):
            bNo = int(blackPictureNo[goalChar[0]][0])
            bx,by = location[int(problemBlackImageNo[0])]
            cur[bx,by] = bNo
            for no in notMatchNo:
                if (no != bNo):
                    whiteNo = no
                    break
            goal = getGoal(whiteNo)
            e = eightDigitalCode(wx,wy,cur,goal)
        else:
            print('Failed!')

    operations,swap = e.solve(problemJson['data']['step'],problemJson['data']['swap'])
    submitData['uuid'] = problemJson['uuid']
    submitData['answer']['operations'] = operations
    if(swap[0] != 0):
        submitData['answer']['swap'] = swap
    ansPost = requests.post(submitUrl ,data = json.dumps(submitData),headers = headers)
    # 测试使用
    if(ansPost):    
        content = ansPost.json()    
    print('\n')
    print(content)
#    print('\nnotMatchCnt = ',notMatchCnt)
#    print('goalChar = ',goalChar)
##    print('\n')

 #   for key,value in match.items():
 #       print(str(key) + '  =  ' + value)
 #   print(e.status())
 #   print('\n')
 #   print('step = ',problemJson['data']['step'])
 #   print('swap = ',problemJson['data']['swap'])
 #   print('uuid = ',problemJson['uuid'])
 #   print('\n')

    print(json.dumps(submitData))
#
    with open('./test/time.txt','r') as fp:
        tstr = fp.read()
    t = int(tstr)
    writeBase64Image('./test/'+str(t)+'.jpg',problemJson['data']['img'])
    saveDictFile(problemJson,'./test/'+str(t)+'.json')
    saveDictFile(content,'./test/'+str(t)+'ans.json')
    with open('./test/time.txt','w') as fp:
        fp.write(str(t+1))        
def solveAll():
    probInfo = getUnfinishedProblem(40)
    for info in probInfo:
        print('author = ',info['author'])
        solveProblem(info['uuid'])


if __name__ == '__main__':
    solveAll()
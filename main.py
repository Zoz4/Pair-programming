import cv2, base64, json, os, requests
import numpy as np
from fileTools import *
from trainTools import *
from imgTools import *
from eightPuzzle import *

if __name__ == '__main__':
    probUrl = 'http://47.102.118.1:8089/api/problem'
    probParams = {'stuid':'171809004'}
    ansUrl = 'http://47.102.118.1:8089/api/answer'
    ansParams = {
        'uuid':'',
        'answer':{
        }
    }
    with open('./test/time.txt','r') as fp:
        tstr = fp.read()
    t = int(tstr)
    print("t = ",t)
    # 得到问题图片，裁剪保存到./target
    problem = requests.get(probUrl,params=probParams)
    problemJson = problem.json()
    writeBase64Image('./test/'+str(t)+'.jpg',problemJson['img'])
    saveDictFile(problemJson,'./test/'+str(t)+'.json')

    #problemJson = readJsonFile('./test/'+str(t)+'.json')
    problemImage = cv2.imread('./test/'+str(t)+'.jpg')

    cutImage(problemImage,'./target')

    # 载入分割的原字符图片到responses（trainLabels）的映射
    charDict = readJsonFile('./record/charDict.json')
    # 载入responses（trainLabels）到分割的原字符图片的映射
    noDict = readJsonFile('./record/noDict.json')
    # 载入分割的原字符图片中的黑色图片所对应的标号如blackPictureNo['a'] == 3
    blackPictureNo = readJsonFile('./record/BlackPictureNo.json')


    # 载入训练数据并训练
    with np.load('./record/knnTrainData.npz') as data:
        trainData = data['trainData']
        responses = data['responses']
    knn = cv2.ml.KNearest_create()
    knn.train(trainData,cv2.ml.ROW_SAMPLE,responses)
    
    problemWhiteImageNo = -1
    problemBlackImageNo = []

    # match[问题图片编号] = 目的图片名称和编号'A1'
    match = {}
    for i in range(1,10):
        image = cv2.imread('./target'+'/'+str(i)+'.jpg')
        corners = getImageTrainData(image)
        if(corners.size < 1):
            # 没有特征点（纯白或纯黑图片）
            if(isWhiteImage(image)):
                problemWhiteImageNo = i
            else:
                problemBlackImageNo.append(i)
        else:
            ret,results,neighbours,dist = knn.findNearest(corners,k=1)
            result = getClosestResult(results)
            match[i] = noDict[str(result)]

    for key,value in match.items():
        print(str(key) + '  =  ' + value)
    
    # 把裁剪后的9张问题图片与原图片的编号对应
    # 编号 0 表示白色图片（被挖去的图片）
    cur = np.full((3,3),0)
    goalChar = ''
    # matchNo 已经被匹配上的原图片的编号集
    matchNo = []
    # notMatchNo 没有被匹配上的图片的编号集
    notMatchNo = []
    # location 图片编号的二维位置
    location = ([-1,-1],[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2])

    # match[问题图片编号] = 目的图片名称和编号'A1'...
    for value in match.values():
        goalChar += value[0]
        matchNo.append(int(value[1]))
    for i in range(1,10):
        if i not in matchNo:
            notMatchNo.append(i)
    notMatchCnt = len(notMatchNo)

    # 对问题图片中已经匹配的图编上原始的编号
    for i in range(1,10):
        if i not in match.keys():
            continue
        x,y = location[i]
        cur[x,y] = int(match[i][1])

    # 问题图片中白色图片的位置
    wx,wy = location[problemWhiteImageNo]


    # 除了白色图片外全部匹配
    if(notMatchCnt == 1):
        # 此时没匹配的图就是白色图片
        whiteNo = notMatchNo[0]
        # 得到图片的目标状态
        goal = getGoal(whiteNo)
        e = eightDigitalCode(wx,wy,cur,goal)
    # 存在一张黑色图片没有匹配    
    elif(notMatchCnt == 2):
        # 原图片中黑色图片的编号和位置
        bNo = int(blackPictureNo[goalChar[0]])
        bx,by = location[int(problemBlackImageNo[0])]
        cur[bx,by] = bNo
 
        for no in notMatchNo:
            if (no != bNo):
                whiteNo = no
                break
        goal = getGoal(whiteNo)

        e = eightDigitalCode(wx,wy,cur,goal)
    # 存在两张黑色图片没有匹配(肯定是F)    
    elif(notMatchCnt == 3):
        # 原图片中两张黑色图片的编号和位置
        bNo1 = int(blakcPictureNo[goalChar[0]])
        bNo2 = int(blackPictureNo[goalChar[0]])
        bx1,by1 = location[int(problemBlackImageNo[0])]
        bx2,by2 = location[int(problemBlackImageNo[1])]

        for no in notMatchNo:
            if((no != bNo1)and(no != bNo2)):
                whiteNo = no
                break
        goal = getGoal(whiteNo)

        cur[bx1,by1] = bNo1
        cur[bx2,by2] = bNo2
        e1 = eightDigitalCode(wx,wy,cur,goal)
        cur[bx1,by1] = bNo2
        cur[bx2,by2] = bNo1
        e2 = eightDigitalCode(wx,wy,cur,goal)    
    else:
        print('impossible')

    print('whiteNo = '+str(whiteNo))
    print(e.status())
    
    print('step = ',problemJson['step'])
    print('swap = ',problemJson['swap'])
    print('uuid = ',problemJson['uuid'])


    if(notMatchCnt <= 2):
        operations,swap = e.solve(problemJson['step'],problemJson['swap'])
        print('operations = ',operations)
        print('myswap = ',swap)
    elif(notMatchCnt == 3):
        operations1,swap1 = e1.solve(problemJson['step'],problemJson['swap'])
        print('operations1 = ',operations1)
        print('myswap1 = ',swap1)
        operations2,swap2 = e2.solve(problemJson['step'],problemJson['swap'])
        print('operations2 = ',operations2)
        print('myswap2 = ',swap2)
        if(len(operations1)>len(operations2)):
            operations = operations2
            swap = swap2
        else:
            operations = operations1
            swap = swap1


    ansParams['uuid'] = problemJson['uuid']
    ansParams['answer']['operations'] = operations
    if(swap[0] != 0):
        ansParams['answer']['swap'] = swap

    print(json.dumps(ansParams))
    ansPost = requests.post(ansUrl,data = json.dumps(ansParams))
    print(ansPost)
    if(ansPost):
        content = ansPost.json()
        print(content)
    with open('./test/time.txt','w') as fp:
        t += 1
        fp.write(str(t))



            




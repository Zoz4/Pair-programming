import cv2, base64, json, os, requests
import numpy as np
from fileTools import *
from trainTools import *
from imgTools import *
from eightPuzzle import *

if __name__ == '__main__':
    probUrl = 'http://47.102.118.1:8089/api/problem'
    probParams = {'stuid':'171809004'}
    headers = {'content-type': "application/json"}
    ansUrl = 'http://47.102.118.1:8089/api/answer'
    ansParams = {
        'uuid':'',
        'answer':{
        }
    }

    # 测试使用
    with open('./test/time.txt','r') as fp: 
        tstr = fp.read()    
    t = int(tstr)   
    problem = requests.get(probUrl,params=probParams)   
    problemJson = problem.json()    
    writeBase64Image('./test/'+str(t)+'.jpg',problemJson['img'])    
    saveDictFile(problemJson,'./test/'+str(t)+'.json')  
    problemImage = cv2.imread('./test/'+str(t)+'.jpg')  
    cutImage(problemImage,'./target')   
    #

    # 从接口得到问题图片
#    problem = requests.get(probUrl,params=probParams)
#    problemJson = problem.json()
#    writeBase64Image('./problem.jpg',problemJson['img'])
#    saveDictFile(problemJson,'./problem.json')

    # 从Json文件中得到问题图片
#    problemJson = readJsonFile('./problem'+'.json')
#    writeBase64Image('./problem'+'.jpg',problemJson['img'])

    # 裁剪问题图片并保存到./target
#    problemImage = cv2.imread('./problem.jpg')
#    cutImage(problemImage,'./target')

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

    # 把裁剪后的9张问题图片与原图片的编号对应
    # 编号 0 表示白色图片（被挖去的图片）
    cur = np.full((3,3),0)
    goalChar = ''
    # matchNo 已经被匹配上的原图片的编号集
    matchNo = []
    # notMatchNo 没有被匹配上的原图片的编号集
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
    # 因为F图片中有两个黑色图片，无法分辨
    # 所以F图片需要独立考虑
    if(goalChar[0] != 'F'):
        if(notMatchCnt == 1):
            # 此时没匹配的图就是白色图片
            whiteNo = notMatchNo[0]
            goal = getGoal(whiteNo)
            e = eightDigitalCode(wx,wy,cur,goal)
        elif(notMatchCnt == 2):
            # 原图片中黑色图片的编号和位置
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

        # 提交答案
        operations,swap = e.solve(problemJson['step'],problemJson['swap'])
        ansParams['uuid'] = problemJson['uuid']
        ansParams['answer']['operations'] = operations
        if(swap[0] != 0):
            ansParams['answer']['swap'] = swap
        ansPost = requests.post(ansUrl ,data = json.dumps(ansParams),headers = headers)
        if(ansPost):    #
            content = ansPost.json()    #

    else:
        if(notMatchCnt == 2):
        # 此时原图片F中两张黑色图片其中一张被挖去,没匹配上的图片为一黑一白
            bx,by = location[int(problemBlackImageNo[0])]
            # 被挖去的黑色图片原编号是notMatch[0]            
            whiteNo0 = notMatchNo[0]
            goal0 = getGoal(whiteNo0)
            cur[bx,by] = notMatchNo[1]
            e0 = eightDigitalCode(wx,wy,cur,goal0)
            # 被挖去的黑色图片原编号是notMatch[1]
            whiteNo1 = notMatchNo[1]
            goal1 = getGoal(whiteNo1)
            cur[bx,by] = notMatchNo[0]
            e1 = eightDigitalCode(wx,wy,cur,goal1)
        elif(notMatchCnt == 3):
        # 此时原图片F中两张黑色图片都没被挖去，没匹配上的图片为两黑一白
            # 原图片中两张黑色图片的编号和位置
            bNo0 = int(blakcPictureNo[goalChar[0]][0])
            bNo1 = int(blackPictureNo[goalChar[0]][1])
            bx0,by0 = location[int(problemBlackImageNo[0])]
            bx1,by1 = location[int(problemBlackImageNo[1])]
            for no in notMatchNo:
                if((no != bNo0)and(no != bNo1)):
                    whiteNo = no
                    break
            goal = getGoal(whiteNo)
            # 第一张黑色问题图片对应第一张没匹配上的黑色图片
            cur[bx0,by0] = bNo0
            cur[bx1,by1] = bNo1
            e0 = eightDigitalCode(wx,wy,cur,goal)
            # 第一张黑色问题图片对应第二张没匹配上的黑色图片
            cur[bx0,by0] = bNo1
            cur[bx1,by1] = bNo0
            e1 = eightDigitalCode(wx,wy,cur,goal)
        else:
            print('Failed!')

        # 提交答案
        ansParams['uuid'] = problemJson['uuid']
        operations,swap = e0.solve(problemJson['step'],problemJson['swap'])
        ansParams['answer']['operations'] = operations
        if(swap[0] != 0):
            ansParams['answer']['swap'] = swap
        ansPost = requests.post(ansUrl ,data = json.dumps(ansParams),headers = headers)
        if(ansPost):    
            content = ansPost.json()    
        
        if(content['score'] != 'true'):
            operations,swap = e1.solve(problemJson['step'],problemJson['swap'])
            ansParams['answer']['operations'] = operations
            if(swap[0] != 0):
                ansParams['answer']['swap'] = swap
            else:
                if('swap' in ansParams['answer'].keys()):
                    del ansParams['answer']['swap']
            ansPost = requests.post(ansUrl ,data = json.dumps(ansParams),headers = headers)
            if(ansPost):    #
                content = ansPost.json()    #

    # 测试使用
    with open('./test/'+str(t)+'ans.json','w')as fp:
        fp.write(json.dumps(content))
    t += 1
    with open('./test/time.txt','w') as fp:
        fp.write(str(t))

    print(content)
    print('\nnotMatchCnt = ',notMatchCnt)
    print('goalChar = ',goalChar)
    print('\n')

    for key,value in match.items():
        print(str(key) + '  =  ' + value)
    if(goalChar[0] != 'F'):
        print(e.status())
    else:
        print(e0.status())
        print(e1.status())
    print('\n')
    print('step = ',problemJson['step'])
    print('swap = ',problemJson['swap'])
    print('uuid = ',problemJson['uuid'])
    print('\n')

    print(json.dumps(ansParams))



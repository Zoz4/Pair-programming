import cv2, base64, json, os, requests, queue
import numpy as np
from fileTools import *
from trainTools import *
from imgTools import *
from eightPuzzle import *


class eightDigitalCode():
    # x , y表示 数字0（被挖去的图片）的位置
    # cur 以数字0~8记录当前图片的状态 （ 3*3 的 ndarray ）
    # goal 为目标状态（字符串表示）
    def __init__(self, x, y, cur, goal):
        self.x = x
        self.y = y
        self.cur = np.copy(cur)
        self.goal = goal
    # 交换两个数字的位置
    def swapCode(self,x1,y1,x2,y2):
        self.cur[x1,y1],self.cur[x2,y2] = self.cur[x2,y2],self.cur[x1,y1]
        if(self.cur[x1,y1] == 0):
            self.x = x1
            self.y = y1
        if(self.cur[x2,y2] == 0):
            self.x = x2
            self.y = y2
    # 模拟白色方块的移动
    def whiteBlockMove(self,op):
        if(op == 'w'):
            nx = self.x - 1
            self.swapCode(self.x,self.y, nx,self.y)
            #self.x = nx
        elif(op == 's'):
            nx = self.x + 1
            self.swapCode(self.x,self.y, nx,self.y)
            #self.x = nx
        elif(op == 'a'):
            ny = self.y - 1
            self.swapCode(self.x,self.y, self.x,ny)
            #self.y = ny
        elif(op == 'd'):
            ny = self.y + 1
            self.swapCode(self.x,self.y, self.x,ny)
            #self.y = ny
    # 以字符串的形式返回当前状态
    def status(self):
        status = ''
        for i in self.cur.flatten():
            status += str(i)
        return status
    # 判断是否达到目标状态
    def isDone(self):
        if self.status() == self.goal:
            return True
        else:
            return False
    def getAllSituations(self,step):
        curStep = 0
        next = [[-1,0],[0,-1],[1,0],[0,1]]
        op = ['w','a','s','d']
        m = np.copy(self.cur)
        situations = {}
        situations[getnum(m)] = ''
        p = Pos(self.x,self.y,m)
        q = queue.Queue()
        q.put(p)
        while(not q.empty()):
            h = q.get()
            if(len(h.s) == step):
                #print(len(h.s))
                break
            for i in range(4):
                tp = Pos(h.x,h.y,h.m,h.s)
                tp.x += next[i][0]
                tp.y += next[i][1]
                if(tp.x<0 or tp.y<0 or tp.x>2 or tp.y>2):
                    continue
                tp.s += op[i]
                tp.m[tp.x,tp.y],tp.m[h.x,h.y] = tp.m[h.x,h.y],tp.m[tp.x,tp.y]
                key = getnum(tp.m)
                if key not in situations.keys():
                    situations[key] = tp.s
                    q.put(tp)
                else:
                    if(len(situations[key]) > len(tp.s)):
                        situations[key] = tp.s


        return situations
    def solve(self, step, swap):
        operations = ''
        mySwap = [0,0]
        operationsDict = readJsonFile('./record'+'/'+self.goal+'.json')
        status = self.status()
        hasSwap = 0
        situations = self.getAllSituations(step)
        #print(situations)
        #print(len(situations))
        minSituation = ''
        minCount = -1
        for situation in situations.keys():
            if(situation == self.goal):
                operations = situations[situation]
                mySwap = [0,0]
                return
            cnt = step-len(situations[situation])
            if( (cnt % 2 ) != 0 ):
                continue
            t1 = list(situation)
            t1[swap[0]-1],t1[swap[1]-1] = t1[swap[1]-1],t1[swap[0]-1]
            afterSwap = ''.join(t1)
            # 经过交换后有解的所有情况
            if afterSwap in operationsDict.keys():
                curCount = max(len(situations[situation]),step) + len(operationsDict[afterSwap])
                if(minCount == -1):
                    hasSwap = 0
                    minSituation = situation
                    minCount = curCount
                else:
                    if(minCount > curCount):
                        hasSwap = 0
                        minSituation = situation
                        minCount = curCount
            # 经过交换后无解的所有情况
            else:
                for i in range(1,9):
                    for j in range(i+1,10):
                        t2 = list(afterSwap)
                        t2[i-1],t2[j-1] = t2[j-1],t2[i-1]
                        afterMySwap = ''.join(t2)

                        if afterMySwap in operationsDict.keys():
                            curCount = max(len(situations[situation]),step) + len(operationsDict[afterMySwap])
                            if(minCount == -1):    
                               hasSwap = 1
                               minSituation = situation
                               minCount = curCount
                               mySwap = [i,j]

                            else:
                                if(minCount > curCount):
                                    hasSwap = 1
                                    minSituation = situation
                                    minCount = curCount
                                    mySwap = [i,j]


        if(len(situations[minSituation]) <= step):
                whiteLocation = minSituation.index('0')+1
                beforeSwapOperations = situations[minSituation]
                cnt = int((step - len(situations[minSituation]))/2)
                if(whiteLocation <= 3):
                    for i in range(0,cnt):
                        beforeSwapOperations += 'sw'
                else:
                    for i in range(0,cnt):
                        beforeSwapOperations += 'ws'
        
        t = list(minSituation)
        t[swap[0]-1],t[swap[1]-1] = t[swap[1]-1],t[swap[0]-1]
        afterSwap = ''.join(t)
        if(hasSwap == 0):
            operations = beforeSwapOperations + operationsDict[afterSwap][::-1]
            mySwap = [0,0]
        else:
            t2 = list(afterSwap)
            t2[mySwap[0]-1],t2[mySwap[1]-1] = t2[mySwap[1]-1],t2[mySwap[0]-1]
            afterMySwap = ''.join(t2)
            operations = beforeSwapOperations + operationsDict[afterMySwap][::-1]
        return operations,mySwap
            






class Pos():
    def __init__(self, x, y, m, s=''):
        self.x = x
        self.y = y
        self.m = np.copy(m)
        self.s = s

def getGoal(cutImageNo):
    if(cutImageNo == 1):
        return '023456789'
    elif(cutImageNo == 2):
        return '103456789'
    elif(cutImageNo == 3):
        return '120456789'
    elif(cutImageNo == 4):
        return '123056789'
    elif(cutImageNo == 5):
        return '123406789'
    elif(cutImageNo == 6):
        return '123450789'
    elif(cutImageNo == 7):
        return '123456089'
    elif(cutImageNo == 8):
        return '123456709'
    elif(cutImageNo == 9):
        return '123456780'
def getnum(m):
    num = ''
    for i in m.flatten():
        num += str(i)
    return num
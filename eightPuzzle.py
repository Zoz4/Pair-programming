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
        elif(op == 's'):
            nx = self.x + 1
            self.swapCode(self.x,self.y, nx,self.y)
        elif(op == 'a'):
            ny = self.y - 1
            self.swapCode(self.x,self.y, self.x,ny)
        elif(op == 'd'):
            ny = self.y + 1
            self.swapCode(self.x,self.y, self.x,ny)
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
    # 得到当前状态下经历一定步数的所有情况
    def getAllSituations(self,step):
        curStep = 0
        next = [[-1,0],[0,-1],[1,0],[0,1]]
        op = ['w','a','s','d']
        m = np.copy(self.cur)
        situations = {}
        p = Pos(self.x,self.y,m)
        situations[p.status()] = ''
        q = queue.Queue()
        q.put(p)
        while(not q.empty()):
            h = q.get()
            if(len(h.s) == step):
                break
            for i in range(4):
                tp = Pos(h.x,h.y,h.m,h.s)
                tp.x += next[i][0]
                tp.y += next[i][1]
                if(tp.x<0 or tp.y<0 or tp.x>2 or tp.y>2):
                    continue
                tp.s += op[i]
                tp.m[tp.x,tp.y],tp.m[h.x,h.y] = tp.m[h.x,h.y],tp.m[tp.x,tp.y]
                status = tp.status()
                if status not in situations.keys():
                    situations[status] = tp.s
                    q.put(tp)
                else:
                    if(len(situations[status]) > len(tp.s)):
                        situations[status] = tp.s
        return situations
    def solve(self, step, swap):
        operations = ''
        mySwap = [0,0]
        # operationsDict[status] 记录当前情况到目标情况的移动步骤
        # 由于是通过目标状态推导
        # operationsDict[status] = 'was....'
        operationsDict = readJsonFile('./record'+'/'+self.goal+'.json')
        hasSwap = 0
        situations = self.getAllSituations(step)
        minStatus = ''
        minCount = -1
        # situations['123045678'] = 'swadas...'
        # 遍历发生强制交换前的所有情况，寻找最短步数的解
        for status in situations.keys():
            # 在强制交换前已经还原
            if(status == self.goal):
                print('没有发生强制交换')
                operations = situations[status]
                mySwap = [0,0]
                return operations,mySwap
            # 统计与强制交换发生的步数差距
            # 差距为偶数步数保留，奇数步数舍去
            cnt = step-len(situations[status])
            if( (cnt % 2 ) != 0 ):
                continue
            # 模拟强制交换，afterSwap:强制交换后的情况
            t1 = list(status)
            t1[swap[0]-1],t1[swap[1]-1] = t1[swap[1]-1],t1[swap[0]-1]
            afterSwap = ''.join(t1)

            # 经过强制交换后有解的所有情况
            if afterSwap in operationsDict.keys():
                curCount = step + len(operationsDict[afterSwap])
                if(minCount == -1):
                    hasSwap = 0
                    minStatus = status
                    minCount = curCount
                else:
                    if(minCount > curCount):
                        hasSwap = 0
                        minStatus = status
                        minCount = curCount
            # 经过强制交换后无解的所有情况
            else:
                # 枚举自由交换的所有情况，afterMySwap:自由交换后的情况
                for i in range(1,9):
                    for j in range(i+1,10):

                        t2 = list(afterSwap)
                        t2[i-1],t2[j-1] = t2[j-1],t2[i-1]
                        afterMySwap = ''.join(t2)

                        if afterMySwap in operationsDict.keys():
                            curCount = step + len(operationsDict[afterMySwap])
                            if(minCount == -1):    
                               hasSwap = 1
                               minStatus = status
                               minCount = curCount
                               mySwap = [i,j]
                            else:
                                if(minCount > curCount):
                                    hasSwap = 1
                                    minStatus = status
                                    minCount = curCount
                                    mySwap = [i,j]
        # 补足交换前没有走够的步数
        if(len(situations[minStatus]) <= step):
                whiteLocation = minStatus.index('0')+1
                beforeSwapOperations = situations[minStatus]
                leftStepsCount = int(  ( step - len(situations[minStatus]) ) / 2  )
                if(whiteLocation <= 3):
                    for i in range(0,leftStepsCount):
                        beforeSwapOperations += 'sw'
                else:
                    for i in range(0,leftStepsCount):
                        beforeSwapOperations += 'ws'
        t1 = list(minStatus)
        t1[swap[0]-1],t1[swap[1]-1] = t1[swap[1]-1],t1[swap[0]-1]
        afterSwap = ''.join(t1)

        # 没有自己交换
        if(hasSwap == 0):
            print('没有自己交换')
            operations = beforeSwapOperations + operationsDict[afterSwap][::-1]
            mySwap = [0,0]
            # 用于触发强制交换
            if(len(operations) == step):
                print('触发强制交换补足')
                operations += 's'
            print('beforeSwapOperations = ',beforeSwapOperations)
            print('afterSwapOperations = ',operationsDict[afterSwap][::-1])
        # 发生自己交换
        else:
            print('发生自己交换')
            t2 = list(afterSwap)
            t2[mySwap[0]-1],t2[mySwap[1]-1] = t2[mySwap[1]-1],t2[mySwap[0]-1]
            afterMySwap = ''.join(t2)
            operations = beforeSwapOperations + operationsDict[afterMySwap][::-1]
            # 用于触发自由交换
            if(len(operations) == step):
                print('触发自由交换补足')
                operations += 'd'
            print('beforeSwapOperations = ',beforeSwapOperations)
            print('afterSwapOperations = ', operationsDict[afterMySwap][::-1])
        return operations,mySwap
            
class Pos():
    def __init__(self, x, y, m, s=''):
        self.x = x
        self.y = y
        self.m = np.copy(m)
        self.s = s
    def status(self):
        status = ''
        for i in self.m.flatten():
            status += str(i)
        return status


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
import queue
import json
import numpy as np

class Pos():
    def __init__(self, x, y, m, s=''):
        self.x = x
        self.y = y
        self.m = np.copy(m)
        self.s = s
def solve():
    move = [[-1,0],[1,0],[0,-1],[0,1]]
    m = np.array([[1,2,3],[4,5,6],[7,8,0]])
    dict = {}
    p = Pos(2,2,m)
    q = queue.Queue()
    q.put(p)
    while( not q.empty() ):
        h = q.get()
        for i in range(4):
            tp = Pos(h.x,h.y,h.m,h.s)
            tp.x += move[i][0]
            tp.y += move[i][1]
            if(tp.x<0 or tp.y<0 or tp.x>2 or tp.y>2):
                continue
            tp.s += step(i)
            tp.m[tp.x,tp.y],tp.m[h.x,h.y] = tp.m[h.x,h.y],tp.m[tp.x,tp.y]
            key = getnum(tp.m)
            if key not in dict.keys():
                dict[key] = tp.s
                q.put(tp)
            else:
                if(len(dict[key]) > len(tp.s)):
                    dict[key] = tp.s
                continue
    with open('./123456780.json','w') as f:
        json.dump(dict, f)

def step(i):
    if(i == 0):
        return 'w'
    elif(i == 1):
        return 's'
    elif(i == 2):
        return 'a'
    elif(i == 3):
        return 'd'
def getnum(m):
    num = ''
    for i in range(3):
        for j in range(3):
            num += str(m[i,j])
    return num

if __name__ == '__main__':
    print('proj.py')
    solve()
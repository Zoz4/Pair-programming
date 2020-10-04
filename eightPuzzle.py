class eightDigitalCode():
    # x , y表示 数字0（被挖去的图片）的位置
    # cur 以数字0~8记录当前图片的状态 （ 3*3 的 ndarray ）
    # goal 为目标状态（字符串表示）
    def __init__(self, x, y, cur, goal):
        self.x = x
        self.y = y
        self.cur = cur.copy(cur)
        self.goal = goal
    # 交换两个数字的位置
    def swap(self,x1,y1,x2,y2):
        self.m[x1,y1],self.m[x2,y2] = self.m[x2,y2],self.m[x1,y1]
    # 模拟白色方块的移动
    def whiteMove(self,op):
        if(op == 'w'):
            nx = self.x - 1
            self.swap(self.x,self.y, nx,self.y)
            self.x = nx
        elif(op == 's'):
            nx = self.x + 1
            self.swap(self.x,self.y, nx,self.y)
            self.x = nx
        elif(op == 'a'):
            ny = self.y - 1
            self.swap(self.x,self.y, self.x,ny)
            self.y = ny
        elif(op == 'd'):
            ny = self.y + 1
            self.swap(self.x,self.y, self.x,ny)
            self.y = ny
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
    
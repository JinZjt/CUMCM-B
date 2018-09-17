import csv
import random
TIME = 545 #cnc worktime
movetime1 = 18 #由题意，移动1步所需时间
movetime2 = 32 #由题意，移动2步所需时间
movetime3 = 46 #由题意，移动3步所需时间
makeuptime0 = 27 #给奇数机器上下料并清洗所需时间
makeuptime1 = 32 #给偶数机器上下料并清洗所需时间
washtime = 25
fault_product_number = []
fault_number = []
fault_begin = []
fault_end = []
class CNC(object):
    def __init__(self, position, Attr,number):
        self.position = position
        self.occupy = 0 #0表示机器上一个加工器件都没有
        self.attr = Attr #1是偶，0是奇
        self.ontime = 0
        self.number = number
    def work(self, rgv):
        if self.occupy == 0:
            self.occupy = 1
            self.ontime = rgv.time
        else:
            if rgv.time - self.ontime >= TIME:  # CNC工作所需时间, 判断是否在工作状态中
                self.ontime = rgv.time


class RGV(object):
    def __init__(self):
        self.currentPosition = 0
        self.time = 0
        self.number = 0
        self.Ontime = []
        self.Offtime = []
    def move(self, place):
        #移动所需时间
        if abs(self.currentPosition - place)==1:
            self.time += movetime1
        if abs(self.currentPosition - place)==2:
            self.time += movetime2
        if abs(self.currentPosition - place)==3:
            self.time += movetime3
        self.currentPosition = place
    def makeup(self, worker): #上下料
        self.Ontime.append(self.time)
        if worker.attr == 0:
            self.time += makeuptime0
        if worker.attr == 1:
            self.time += makeuptime1
        if worker.occupy == 1:
            self.number +=1
            self.Offtime.append(self.time)
    def wash(self):
        self.time += washtime
    def stay(self,workers):
        flag = False
        worktime=[]
        for i in range(1,9):#记录各机器的开始工作时间
            worktime.append(workers[i].ontime)
        temp = min(worktime)
        while flag == False:
            self.time +=1 #时间继续走，rgv停在原地，尽量少移动
            if self.time - temp >= TIME: #检验是否有空闲机器出现
                flag = True


#初始化8台CNC和RGV
cnc = [0]
cnc.append(CNC(1, 0, 1))
cnc.append(CNC(1, 1, 2))
cnc.append(CNC(2, 0, 3))
cnc.append(CNC(2, 1, 4))
cnc.append(CNC(3, 0, 5))
cnc.append(CNC(3, 1, 6))
cnc.append(CNC(4, 0, 7))
cnc.append(CNC(4, 1, 8))
rgv = RGV()
workerused = []

while rgv.number >= 0:
    if rgv.time >= 28800:
        break
    dist = 10
    pointer = 0
    list  = []
    for j in range(1, 5):
        if cnc[2*j-1].occupy == 0 or cnc[2*j].occupy == 0:
            list.append(j)
        elif rgv.time - cnc[2*j-1].ontime >= TIME or rgv.time - cnc[2*j].ontime >= TIME:
            list.append(j)
    if list ==[]:
        rgv.stay(cnc)
        continue

    for i in list:#先记录距离
        if i != rgv.currentPosition:
            temp = abs(i - rgv.currentPosition)
            if temp <= dist:
                dist = temp
                pointer = i  # 记录离当前rgv最近的CNC的位置
        else:
            if cnc[2*i-1].occupy == 0 or cnc[2*i].occupy == 0 or rgv.time - cnc[2*i-1].ontime>=TIME or rgv.time - cnc[2*i].ontime >=TIME:
                pointer = i
                break
#正式工作部分
    if cnc[2*pointer-1].occupy == 0:
        rgv.move(pointer)
        workerused.append(2*pointer-1)
        rgv.makeup(cnc[2*pointer-1])
        cnc[2 * pointer - 1].work(rgv)
        rgv.wash()
    elif cnc[2*pointer-1].occupy == 1 and rgv.time - cnc[2*pointer-1].ontime >= TIME:
        rgv.move(pointer)
        workerused.append(2*pointer-1)
        rgv.makeup(cnc[2*pointer-1])
        cnc[2 * pointer-1].work(rgv)
        rgv.wash()
    elif cnc[2*pointer].occupy == 0:
        rgv.move(pointer)
        workerused.append(2*pointer)
        rgv.makeup(cnc[2*pointer])
        cnc[2 * pointer].work(rgv)
    elif cnc[2*pointer].occupy == 1 and rgv.time - cnc[2*pointer].ontime >= TIME:
        rgv.move(pointer)
        workerused.append(2*pointer)
        rgv.makeup(cnc[2*pointer])
        cnc[2 * pointer].work(rgv)
        rgv.wash()

print(rgv.number,len(fault_number))
#print(workerused)
path = r"C:\Users\JonathanZ\Desktop\cumcm\data3.csv"
pathfault = r"C:\Users\JonathanZ\Desktop\cumcm\data4fault.csv"
number = rgv.number

with open(path, "w+", newline='') as f:
    headers = ['productnumber','ontime','offtime']
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for i in range(number):
        row = (i+1, rgv.Ontime[i], rgv.Offtime[i])
        f_csv.writerow(row)
'''
with open(pathfault, 'w+', newline='') as f:
    headers = ['product number','fault number','fault begin','fault end']
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for i in range(len(fault_number)):
        row = (fault_product_number[i],fault_number[i], fault_begin[i], fault_end[i])
        f_csv.writerow(row)
'''

























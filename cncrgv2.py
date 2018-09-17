import csv
import random
TIME1 = 400 #cnc worktime1
TIME2 = 378 #cnc worktime2
movetime1 = 20 #由题意，移动1步所需时间
movetime2 = 33 #由题意，移动2步所需时间
movetime3 = 46 #由题意，移动3步所需时间
makeuptime0 = 28 #给奇数机器上下料并清洗所需时间
makeuptime1 = 31 #给偶数机器上下料并清洗所需时间
washtime = 25
fault_product_number = []
fault_number = []
fault_begin = []
fault_end = []
FLAG = 1
can1 = [1,3,5,7]
can2 = [2,4,6,8]
candidate1 = {1:1,3:2,5:3,7:4}
candidate2 = {2:1,4:2,6:3,8:4}
workerused1 = []
workerused2 = []
class CNC(object):
    def __init__(self, position, Attr,number):
        self.position = position
        self.occupy = 0 #0表示机器上一个加工器件都没有
        self.attr = Attr #1是偶，0是奇
        self.ontime = 0
        self.number = number
    def work(self, rgv):
        clue = 0
        factor1 = random.randint(0,999)
        if factor1<399 and factor1>=299:
            clue = 1
        if clue!=1:
            if self.occupy == 0:
                self.occupy = 1
                self.ontime = rgv.time
            elif self.occupy == 1 and self.number in can1:
                if rgv.time - self.ontime >= TIME1:  # CNC工作所需时间, 判断是否在工作状态中
                    self.ontime = rgv.time
            elif self.occupy == 1 and self.number in can2:
                if rgv.time - self.ontime >= TIME2:
                    self.ontime = rgv.time
        else:
            factor2 = random.randint(600,1201)
            fault_product_number.append(rgv.number)
            fault_number.append(self.number)
            fault_begin.append(self.ontime)
            self.occupy = 1
            self.ontime += factor2
            fault_end.append(self.ontime)


class RGV(object):
    def __init__(self):
        self.currentPosition = 0
        self.time = 0
        self.number = 0
        self.Ontime1 = []
        self.Offtime1 = []
        self.Ontime2 = []
        self.Offtime2 = []
    def move(self, place):
        #移动所需时间
        if abs(self.currentPosition - place)==1:
            self.time += movetime1
        if abs(self.currentPosition - place)==2:
            self.time += movetime2
        if abs(self.currentPosition - place)==3:
            self.time += movetime3
        self.currentPosition = place
    def makeup1(self, worker): #上下料
        self.Ontime1.append(self.time)
        if worker.attr == 0:
            self.time += makeuptime0
        if worker.attr == 1:
            self.time += makeuptime1
        if worker.occupy == 1:
            self.Offtime1.append(self.time)
    def makeup2(self, worker): #上下料
        self.Ontime2.append(self.time)
        if worker.attr == 0:
            self.time += makeuptime0
        if worker.attr == 1:
            self.time += makeuptime1
        if worker.occupy == 1:
            self.number +=1
            self.Offtime2.append(self.time)
    def wash(self):
        self.time += washtime
    def stay1(self,workers):
        flag = False
        worktime=[]
        for i in can1:#记录各机器的开始工作时间
            worktime.append(workers[i].ontime)
        temp = min(worktime)
        while flag == False:
            self.time +=1 #时间继续走，rgv停在原地，尽量少移动
            if self.time - temp >= TIME1: #检验是否有空闲机器出现
                flag = True

    def stay2(self,workers):
        flag = False
        worktime=[]
        for i in can2:#记录各机器的开始工作时间
            worktime.append(workers[i].ontime)
        temp = min(worktime)
        while flag == False:
            self.time +=1 #时间继续走，rgv停在原地，尽量少移动
            if self.time - temp >= TIME2: #检验是否有空闲机器出现
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
    list1  = []
    list2 = []
    for j in can1:
        temp1 = candidate1[j]
        if cnc[j].occupy == 0:
            list1.append(temp1)
        elif rgv.time - cnc[j].ontime >= TIME1:
            list1.append(temp1)
    if FLAG == 1 and list1 ==[]:
        rgv.stay1(cnc)
        continue
    if FLAG == 1:
        for i in list1:  # 先记录距离
            if i != rgv.currentPosition:
                temp = abs(i - rgv.currentPosition)
                if temp <= dist:
                    dist = temp
                    pointer = i  # 记录离当前rgv最近的CNC的位置
            else:
                if cnc[2 * i - 1].occupy == 0 or rgv.time - cnc[2 * i - 1].ontime >= TIME1:
                    pointer = i
                    break
        # 正式工作部分
        if cnc[2 * pointer - 1].occupy == 0:
            rgv.move(pointer)
            # workerused.append(2*pointer-1)
            rgv.makeup1(cnc[2 * pointer - 1])
            cnc[2 * pointer - 1].work(rgv)
            workerused1.append(2*pointer -1)
            rgv.wash()
            FLAG = 2
        elif cnc[2 * pointer - 1].occupy == 1 and rgv.time - cnc[2 * pointer - 1].ontime >= TIME1:
            rgv.move(pointer)
            # workerused.append(2*pointer-1)
            rgv.makeup1(cnc[2 * pointer - 1])
            cnc[2 * pointer - 1].work(rgv)
            workerused1.append(2*pointer -1)
            rgv.wash()
            FLAG = 2


    for j in can2:
        temp2 = candidate2[j]
        if cnc[j].occupy == 0:
            list2.append(temp2)
        elif rgv.time - cnc[j].ontime >= TIME2:
            list2.append(temp2)

    if FLAG == 2 and list2 == []:
        rgv.stay2(cnc)
        continue
    if FLAG ==2:
        for i in list2:  # 先记录距离
            if i != rgv.currentPosition:
                temp = abs(i - rgv.currentPosition)
                if temp <= dist:
                    dist = temp
                    pointer = i  # 记录离当前rgv最近的CNC的位置
            else:
                if cnc[2 * i].occupy == 0 or rgv.time - cnc[2 * i].ontime >= TIME2:
                    pointer = i
                    break
        # 正式工作部分
        if cnc[2 * pointer].occupy == 0:
            rgv.move(pointer)
            # workerused.append(2*pointer-1)
            rgv.makeup2(cnc[2 * pointer])
            cnc[2 * pointer].work(rgv)
            workerused2.append(2*pointer)
            rgv.wash()
            FLAG = 1
        elif cnc[2 * pointer].occupy == 1 and rgv.time - cnc[2 * pointer].ontime >= TIME2:
            rgv.move(pointer)
            # workerused.append(2*pointer-1)
            rgv.makeup2(cnc[2 * pointer])
            cnc[2 * pointer].work(rgv)
            workerused2.append(2*pointer)
            rgv.wash()
            FLAG = 1

print(rgv.number,len(rgv.Ontime1),len(rgv.Offtime1),len(fault_product_number),len(fault_number),len(fault_begin))
path = r"C:\Users\JonathanZ\Desktop\cumcm\twoDATA3.csv"
pathfault = r"C:\Users\JonathanZ\Desktop\cumcm\twoDATA3fault.csv"

with open(path, "w+", newline='') as f:
    headers = ['productnumber','ontime1','offtime1','ontime2','offtime2']
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for i in range(rgv.number):
        row = (i+1, rgv.Ontime1[i], rgv.Offtime1[i], rgv.Ontime2[i], rgv.Offtime2[i])
        f_csv.writerow(row)

with open(pathfault, 'w+', newline='') as f:
    headers = ['product number','fault number','fault begin','fault end']
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for i in range(len(fault_number)):
        row = (fault_product_number[i],fault_number[i], fault_begin[i], fault_end[i])
        f_csv.writerow(row)

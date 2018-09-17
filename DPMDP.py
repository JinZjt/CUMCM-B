import numpy as np
import copy
import matplotlib.pyplot as plt
def policy_iteration(p_h, theta = 0.0001, discount_factor = 1.0):
    value = np.zeros(28800)
    location = np.zeros(28800)
    workstate = np.zeros((9, 28800))#第0行置零，个人习惯，怕数错，脑子记不住，实际cnc工作状态的记录从第一行开始
    position = 0  # RGV所在位置，初始化为0
    WorkTime = 560 #CNC工作时间
    Makeuptime1 = 53 #上下料加清洗的时间，偶数次机器
    Makeuptime2 = 56 #上下料加清洗的时间，奇数次机器

    def rewardDetermination(currentposition, workstate, s): #s是当前时间秒
        workerposition = [0,1,1,2,2,3,3,4,4]
        dist = []
        reward = []
        for i in range(1,9):
            dist.append(abs(workerposition[i]-currentposition))
        length = len(dist)
        for j in range(length):
            if dist[j] == 0 :
                reward.append(-1)
            elif j%2 == 0 and dist[j] == 1:
                reward.append(-1)
            elif j%2 == 1 and dist[j] == 1:
                reward.append(-1.5)
            elif j%2 == 0 and dist[j] == 2:
                reward.append(-2)
            elif j%2 == 1 and dist[j] == 2:
                reward.append(-2.5)
            elif j%2 == 0 and dist[j] == 3:
                reward.append(-3)
            elif j%2 == 1 and dist[j] == 3:
                reward.append(-3.5)
            elif j%2 == 0 and dist[j] == 4:
                reward.append(-4)
            elif j%2 == 1 and dist[j] == 4:
                reward.append(-4.5)
        for k in range(1,9):
            if workstate[k][s] == 1 and position == k: #如果移动到了正在工作的CNC上也算空置，予以惩罚;
                reward[k-1] -= 100
            if workstate[k][s] == 0 and workstate[k][s+1] == 0: #处理闲置的这个地方，想了一下，应该给予鼓励，因为要是惩罚的话，后面几号的reward很难超过前几号，这会导致计算机认为呆在前面几号，哪怕原地不动，也比到后面几号强，这样就会导致机器资源的浪费。
                reward[k-1] += 1.1
        return reward
    def one_step_look_ahead(s,V,rewards):
        A = np.zeros(8)
        for i in range(8):
            A[i] += p_h*(rewards[i]+discount_factor*V[s+1]) #根据bellman可得
        return A
    #flag = 1
    s = 0
    while True:
        delta = 0
        while s <28799:
            if position == 0:
                coordinate = 0
            elif position == 1 or position == 2:
                coordinate = 1
            elif position == 3 or position == 4:
                coordinate = 2
            elif position == 5 or position ==6:
                coordinate = 3
            elif position == 7 or position ==8:
                coordinate = 4
            rewards = rewardDetermination(coordinate, workstate, s)#因为要考虑到距离和奇偶以及工作状态，所以先进行reward的判断
            A = one_step_look_ahead(s,value,rewards) # one step lookahead to find best action for this state(second)
            best_action_value = np.max(A) #找到best action所带来的best value
            p = np.argmax(A)#找到最大值所对应的索引
            if p==0 or p==1:
                bestposition = 1
            elif p==2 or p==3:
                bestposition = 2
            elif p==4 or p==5:
                bestposition = 3
            elif p==6 or p==7:
                bestposition = 4#记录best action所指向的cnc的实际位置

            distance = bestposition - position
            if distance == 1:
                movetime  = 20
            elif distance == 2:
                movetime = 33
            elif distance == 3:
                movetime = 46
            elif distance == 0:
                movetime = 0
            position = np.argmax(A)+1# 移动到best action对应的cnc面前
            if (position)%2 == 1:
                makeuptime = Makeuptime1
            else:
                makeuptime = Makeuptime2
            for i in range(WorkTime):#cnc工作时把它的状态标记为1，代表正在工作
                if s+i >= 28800:
                    break
                workstate[position][s+i] = 1
            for i in range(makeuptime):#假定上下料并清洗的过程，rgv全程呆在对应的cnc面前不移动。
                if s+i >= 28800:
                    break
                location[s+i] = position
            delta = max(delta, np.abs(best_action_value - value[s]))
            value[s] = best_action_value #更新当前的value
            s += makeuptime+movetime#更新时间
            #print(s)
        #print(flag)
        #flag += 1

        if delta < theta:
            #小于阈值，结束训练
            break
    return location, value
    # 根据location判断rgv都找哪台cnc工作过，实际上就是policy了。

policy, V= policy_iteration(0.125)
print(policy[:1000])
'''flag = 0
for i in policy:
    if i == 0:
        flag+=1
print(flag)
'''
'''def search(a):
    s=[]
    length =len(a)
    flag = a[0]
    for i in range(length):
        if i >= 1 and flag == a[i]:
            continue
        elif i >= 1 and flag != a[i]:
            flag = a[i]
        s.append(a[i])
    return s
count = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
s = search(policy)
print(s)
for i in range(9):
    for j in s:
        if j in count:
            count[j]+=1
print(count)
'''
'''
plt.plot()
plt.plot(V[1000:2000])
plt.title("Value - Reward")
plt.ylabel("Value")
plt.show()
'''













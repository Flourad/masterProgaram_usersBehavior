# coding: utf-8
#读取构造的数据，根据用户的行为模型和兴趣模型对数据进行处理

import numpy as np
from numpy import arange
import math

# 读取构造的数据文件，将其保存于自己构造的数据结构user_data中
def read_file():

    user_data= {}  #存储从文件中读取出的每一行，key：UID，value：嵌套列表: [演出ID,页面停留时间,翻页/滚动次数,收藏次数,购票张数]
    rf = open("user_data.txt","r")

    try:
        for line in rf.readlines():    #依次读取每一行
            line.strip()                #去掉每行头尾空行
            if line.find("UID") != -1:   #跳过包含不是用户记录的行，即包含UID的行（==-1表示没找到）
                continue    
            tmp = line.split(',')       #用逗号来分割读取数据每行中的字符串，分割后返回列表
            uid = tmp[0]
            if uid not in user_data:    #初始化字典的key对应的字典
                user_data[uid] = []
            user_data[uid].append([tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]])
    finally:
        rf.close()

    return user_data

#对原始数据进行处理，首先计算每种行为对应的权值：1.数据归一化 2.计算熵值 3.计算熵权，然后根据用户兴趣模型得到用户的兴趣矩阵
def gener_interestMatrix(user_data):
    dic_sum = {}
    user_behavior = {}  #用户行为字典，key:UID value: 嵌套字典 [演出ID,页面停留时间,翻页/滚动次数,收藏次数,购票张数] 
                        #与user_data有区别，user_data中演出ID有重复，而这里没有，对一个用户的所有记录中相同的演出的行为数据已经进行了累加处理

    for uid, recList in user_data.items():
        if uid not in user_behavior.items():
            user_behavior[uid] = []

        dic_rec = {}    #一个用户的行为记录字典,key:演出id value: 嵌套的列表 该演出对应的行为数据 [页面停留时间,翻页/滚动次数,收藏次数,购票张数]
        for rec in recList:  #recList代表一个用户的所有记录的列表
            if rec[0] not in dic_rec:  #item[0]表示演出ID
                dic_rec[rec[0]] = []
            dic_rec[rec[0]].append([rec[1], rec[2], rec[3], rec[4]])

        for sid, bdata in dic_rec.items():
            stayTime = 0
            pageNum = 0
            collectNum = 0
            buyNum = 0
            count = 0
            for data in bdata:
                count += 1
                stayTime += int(data[0])
                pageNum += int(data[1])
                if(data[2] == '1'):
                    collectNum += 1
                buyNum += int(data[3])
            user_behavior[uid].append([int(sid),stayTime/count,pageNum,collectNum,buyNum])

    user_interest = {}  #用户兴趣字典，key:UID value:二维矩阵 第一行是一个用户对应的所有演出ID 第二行表示与第一行演出ID对应的兴趣值
    for uid,ub in user_behavior.items():
        a = np.array(ub)    #讲用户行为对应的嵌套的列表转换成矩阵，这里用到了numpy包中的array函数
        firstColumn = a[:,0] #获取矩阵的第一列
        b = np.delete(a,0,1) #删除矩阵的第一列
        c = normalize_bycolumn(b,2.0,1.0)   #矩阵列归一化
        # d = np.insert(c, 0, firstColumn, axis = 1)
        # 下面用到了熵权法中的各种公式
        s = c.sum(axis = 0) #对归一化矩阵中的每一列进行求和
        p = np.divide(c,s)
        tmp = p *  np.log(p)
        e = -(1/np.log(4)) * tmp.sum(axis = 0)
        bw = np.divide((1 - e),4-e.sum(axis = 0))
        f = c * bw 
        r = np.vstack((firstColumn, f.sum(axis = 1))) #将两个矩阵进行拼接，按照行进行拼接
        user_interest[uid] = r

    for i,j in user_interest.items():
        print i
        print j

#矩阵归一化函数
def normalize_bycolumn(myarray,high,low):
    mins = np.min(myarray, axis = 0)  #求矩阵列中的最小值
    maxs = np.max(myarray, axis = 0)  #求矩阵列中得最大值
    aveg = maxs - mins 
    return high - (((high - low) * (maxs - myarray)) / aveg)

if __name__ == "__main__":
    dic_rflie = read_file()
    gener_interestMatrix(dic_rflie)

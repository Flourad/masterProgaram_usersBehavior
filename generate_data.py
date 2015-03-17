# coding: utf-8
# 该模块生成用户行为数据
# UID 演出ID 页面停留时间 翻页/滚动次数 是否收藏 购买张数

from random import choice
import random

fo = open("user_data.txt","w")

fo.write("UID，ShowID, StayTime, PageNum, IsStored, TicketsNum")
fo.write('\n')

IsStored = [0,1]#1表示收藏，0表示未收藏

for uid in range(1,501):#用户量为500
    for c in range(random.randint(10,50)):#每个用户产生的记录条数
        fo.write(str(uid))
        fo.write(',')
        fo.write(str(random.randint(1,20)))#演出ID
        fo.write(',')
        NumList = [0,random.randint(1,20)]  
        fo.write(str(random.randint(10,3000))) #页面停留时间
        fo.write(',')
        fo.write(str(random.randint(1,50)))   #翻页/滚动次数
        fo.write(',')
        fo.write(str(random.choice(IsStored))) #是否收藏演出
        fo.write(',')
        fo.write(str(random.choice(NumList)))  #购票张数
        fo.write('\n')
fo.close()

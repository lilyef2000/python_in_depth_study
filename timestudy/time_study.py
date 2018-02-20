# _*_ coding:utf-8 _*_
__author__ = 'antenna'
__date__ = '18-2-20 下午8:08'

import time

print("---time.time()从1970-01-01 00:00:00 UTC，开始到现在所经历的时间，以浮点数的'秒'来表示---")
print(time.time())
print("---time.gmtime()用结构化的时间组（year,month,day,hours,minutes,seconds....）来表示从1970-01-01 00:00:00 UTC，开始到现在所经历的时间.---")
print(time.gmtime())
print("---time.localtime()用结构化的时间组，表示本地时间---")
print(time.localtime())
print("---time.ctime()用字符串string类型表示时间。---")
print(time.ctime())
print("---time.mktime()将本地时间列表转化为浮点数的秒来表示---")
print(time.mktime(time.localtime()))
print("---time.strftime()将时间组时间转化为指定格式的String类---")
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
print("---time.strptime()将String类时间转化为时间组格式---")
print(time.strptime(time.ctime()))

def run():
    start = time.time()
    for i in range(1000):
        j = i * 2
        for k in range(j):
            t = k
            # print(t)
    end = time.time()
    print('(run)程序执行时间: ',end - start)

def run2():
    start = time.clock()
    for i in range(1000):
        j = i * 2
        for k in range(j):
            t = k
            # print(t)
    end = time.clock()
    print('(run2)CPU执行时间: ',end - start)

def run3():
    start = time.clock()
    for i in range(1000):
        j = i * 2
        for k in range(j):
            t = k
    end = time.clock()
    print('(run3)CPU执行时间: ',end - start)

run()
run2()
run3()
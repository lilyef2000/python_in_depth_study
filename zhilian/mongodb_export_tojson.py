# _*_ coding:utf-8 _*_
__author__ = 'antenna'
__date__ = '18-2-18 下午4:27'
import os
import json

def file(str_f):
    list = []
    with open(str_f, 'r',encoding='utf-8') as f:
        for line in f.readlines():
            dic = json.loads(line)
            list.append(dic)

    return list


if __name__ == '__main__':

    # mongodb采集结果导出到json文件
    result = os.system("D:\\mongodb\\bin\\mongoexport.exe  -d zhilian -c python -o  ./Python_nation.json")
    print(result)


    # json文件转换
    # dict = {}
    # list = file("Python_nation.json")
    # dict['jobs'] = list
    # print(dict)




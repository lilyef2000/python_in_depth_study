# _*_ coding:utf-8 _*_
__author__ = 'antenna'
__date__ = '18-2-19 上午9:13'

from pandas.io.json import json_normalize
import pandas as pd
import json
import time

# 读入数据
data_str = open('Python_nation.json',encoding='utf-8').read()
print(data_str)

# # 测试json_normalize
# start_time = time.time()
# for i in range(0, 300):
#     data_list = json.loads(data_str)
#     df = json_normalize(data_list)
# end_time = time.time()
# print
# end_time - start_time
#
# # 测试自己构造
# start_time = time.time()
# for i in range(0, 300):
#     data_list = json.loads(data_str)
#     data = [[d['timestamp'], d['value']] for d in data_list]
#     df = pd.DataFrame(data, columns=['timestamp', 'value'])
# end_time = time.time()
# print
# end_time - start_time
#
#  测试read_json
start_time = time.time()
# for i in range(0, 300):

# end_time = time.time()
# print(end_time - start_time)

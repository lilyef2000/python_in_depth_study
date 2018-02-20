# _*_ coding:utf-8 _*_
__author__ = 'antenna'
__date__ = '18-2-18 下午8:27'

from pandas.io.json import json_normalize
import pandas as pd
import json
import time
import codecs


# 读入文件名
import_from = 'Python_nation.json'
export_to   = './Python_nation.xls'

start_time = time.time()
# 读入json文件并做简单处理
with open(import_from, 'r', encoding="utf-8") as json_file:
    df = pd.read_json(json_file)
    # df.info()
    # print(df[['_id', '公司名称']].head())
    df.index = df['_id']
    del (df['_id'])
    df1 = df.sort_index()
    df = df1
    df.to_excel(export_to)


end_time = time.time()
print(end_time - start_time)
print("已成功导出至文件%s" % export_to)


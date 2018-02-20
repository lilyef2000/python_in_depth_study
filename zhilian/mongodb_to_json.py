# _*_ coding:utf-8 _*_
__author__ = 'antenna'
__date__ = '18-2-18 下午9:50'

import json
import pymongo
from zhilian.zhilian_kw_config import *
from bson import json_util

# 建立连接
client = pymongo.MongoClient(MONGO_URI)
# 指定数据库
db = client[MONGO_DB]
# 指定集合
collection = db[KEYWORDS[0]]
# 指定要查询的内容
result = collection.find()

# 将查询结果格式化成list格式result_list
result_list  = list(result)
# 将查询结果格式化成json格式(因为_id为mongodb对象格式，需转化为json才能进一步处理)
json_str = json.dumps(result_list,default=json_util.default,ensure_ascii = False)
# 将json子串转化为list格式result_list_1
result_list_1 = json.loads(json_str, encoding='utf-8')
# 将_id字段中的$oid的值赋给_id最终生成result_list_2
result_list_2 = []
for list_temp in result_list_1:
    print(list_temp['_id']['$oid'])
    list_temp['_id'] = (list_temp['_id']['$oid'])
    result_list_2.append(list_temp)
# print(result_list_2)

# 将结果result_list_2 json格式化并存储进json文件
with open('Python_nation.json','w',encoding='utf-8') as json_file:
    # json_file.write(json.dumps(result_list, default=json_util.default, ensure_ascii=False))
    json.dump(result_list_2,json_file,default=json_util.default,ensure_ascii = False)




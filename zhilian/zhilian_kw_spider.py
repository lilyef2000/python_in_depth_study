# _*_ coding:utf-8 _*_
# Code based on Python 3.x
# __author__ = 'antenna'
# __date__ = '18-2-18 下午12:09'


from datetime import datetime
from urllib.parse import urlencode
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import pymongo
from zhilian.zhilian_kw_config import *
import time
from itertools import product
import random

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    response = requests.get(url, headers=headers)
    delay = random.randint(0, 2)
    time.sleep(delay)  # 设置等待时间，防止网站反爬虫
    return response.text

def get_content(html):
    # 记录保存日期
    date = datetime.now().date()
    date = datetime.strftime(date, '%Y-%m-%d')  # 转变成str

    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    data_main = body.find('div', {'class': 'newlist_list_content'})

    if data_main:
        tables = data_main.find_all('table')

        for i, table_info in enumerate(tables):
            if i == 0:
                continue
            tds = table_info.find('tr').find_all('td')
            zwmc = tds[0].find('a').get_text()  # 职位名称
            zw_link = tds[0].find('a').get('href')  # 职位链接
            fkl = tds[1].find('span').get_text()  # 反馈率
            gsmc = tds[2].find('a').get_text()  # 公司名称
            zwyx = tds[3].get_text()  # 职位月薪
            gzdd = tds[4].get_text()  # 工作地点
            gbsj = tds[5].find('span').get_text()  # 发布日期

            tr_brief_spans = table_info.find('tr', {'class': 'newlist_tr_detail'}).find_all('span')

            gsdd = ""
            gsxz = ""
            gsgm = ""
            gzjy = ""
            xlyq = ""
            zwyx_1 = ""
            for list in tr_brief_spans:
                if len(list.get_text().split('：')) >= 2:
                    if list.get_text().split('：')[0] == "地点":
                        gsdd = list.get_text().split('：')[1]  # 公司地点
                    elif list.get_text().split('：')[0] == "公司性质":
                        gsxz = list.get_text().split('：')[1]  # 公司性质
                    elif list.get_text().split('：')[0] == "公司规模":
                        gsgm = list.get_text().split('：')[1]  # 公司规模
                    elif list.get_text().split('：')[0] == "经验":
                        gzjy = list.get_text().split('：')[1]  # 工作经验
                    elif list.get_text().split('：')[0] == "学历":
                        xlyq = list.get_text().split('：')[1]  # 学历要求
                    elif list.get_text().split('：')[0] == "职位月薪":
                        zwyx_1 = list.get_text().split('：')[1]  # 职位月薪(元/月)
                    else:
                        break

            tr_brief = table_info.find('tr', {'class': 'newlist_tr_detail'})
            # 招聘简介
            brief = tr_brief.find('li', {'class': 'newlist_deatil_last'}).get_text()

            # 用生成器获取信息
            yield {'职位名称': zwmc,  # 职位名称
                   '反馈率': fkl,  # 反馈率
                   '公司名称': gsmc,  # 公司名称
                   '职位月薪': zwyx,  # 职位月薪
                   '工作地点': gzdd,  # 工作地点
                   '公布时间': gbsj,  # 公布时间
                   '招聘简介': brief,  # 招聘简介
                   '职位链接': zw_link,  # 网页链接
                   '保存时间': date,  # 记录信息保存的日期
                   '公司地点': gsdd,  # 公司地点
                   '公司性质': gsxz,  # 公司性质
                   '公司规模': gsgm,  # 公司规模
                   '工作经验': gzjy,  # 工作经验
                   '学历要求': xlyq,  # 学历要求
                   '职业薪水': zwyx_1,  # 职位月薪(元/月)

                   }

def main(args):
    basic_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'

    for keyword in KEYWORDS:
        mongo_table = db[keyword]
        paras = {'jl': args[0],
                 'kw': keyword,
                 'p': args[1]  # 第X页
                 }
        url = basic_url + urlencode(paras)
        # print(url)
        html = download(url)
        # print(html)
        if html:
            data = get_content(html)
            for item in data:
                if mongo_table.update({'职位链接': item['职位链接']}, {'$set': item}, True):
                    print('已保存记录：', item)

if __name__ == '__main__':
    start = time.time()
    number_list = list(range(TOTAL_PAGE_NUMBER))
    args = product(ADDRESS, number_list)
    pool = Pool()
    pool.map(main, args) # 多进程运行
    end = time.time()
    print('Finished, task runs %s seconds.' % (end - start))
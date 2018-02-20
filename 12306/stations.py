# _*_ coding:utf-8 _*_
__author__ = 'antenna'
__date__ = '18-2-20 下午8:39'

import re
import requests
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
requests.packages.urllib3.disable_warnings()#如果不加此句会有：InsecureRequestWarning: Unverified HTTPS request is being made
html = requests.get(url,verify=False)
station = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', html.text)
stations = dict(station)
pprint(stations,indent = 4)
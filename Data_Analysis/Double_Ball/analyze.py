#!/bin/env python3.7
#   Version: v1.0.1
#   Filename: test.py
#   Author: Linux - hello_linux@aliyun.com
#   Description: ---
#   Create: 2018-08-09 18:29:10
"""
Require modules: beautifulsoup4,requests,time,csv

Describe:
    search information for Double Ball
"""
from bs4 import BeautifulSoup
import requests
import time
import csv

URL = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_%s.html'
URLS = (URL % i for i in range(1, 10))
ALLURLS = list(URLS)

HEADERS = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4337.400 QQBrowser/9.7.12672.400',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8'}

COOKIES = {'Cookie': 'Hm_lvt_692bd5f9c07d3ebd0063062fb0d7622f=1521165246; \
           Hm_lpvt_692bd5f9c07d3ebd0063062fb0d7622f=1521165250;\
           _ga=GA1.2.1791969145.1521165246;\
           _gid=GA1.2.1551924898.1521165246'}

for i in ALLURLS:  # 遍历网址并执行以下操作
    time.sleep(3)  # 不能捣乱哦，必须加一个延时
    r = requests.get(str(i), headers=HEADERS, cookies=COOKIES)
    r.encoding == 'utf-8'  # 解决乱码的问题

    soup = BeautifulSoup(r.text, "lxml")  # 转化成LXML格式
    ceshi = soup.select("tr td")
    ceshi1 = ceshi[::7]  # 因为标签的问题，采用切片的方式获得想要的数据，也可以用find__all加正则采集
    ceshi2 = ceshi[1::7]
    haoma = soup.select("tr td em")
    hong1 = haoma[0::7]
    hong2 = haoma[1::7]
    hong3 = haoma[2::7]
    hong4 = haoma[3::7]
    hong5 = haoma[4::7]
    hong6 = haoma[5::7]
    lan1 = haoma[6::7]

    print(i)  # 用控制台监视已经爬过了多少网址

    for i, j, h1, h2, h3, h4, h5, h6, l1 in zip(ceshi1, ceshi2, hong1, hong2, hong3, hong4, hong5, hong6, lan1):
        with open('egg.csv', 'a', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [i.string, j.string, h1.string, h2.string, h3.string, h4.string, h5.string, h6.string, l1.string])

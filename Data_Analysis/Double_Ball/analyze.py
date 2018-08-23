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
URLS = (URL % i for i in range(1, 5))
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

for i in ALLURLS:
    time.sleep(3)
    r = requests.get(str(i), headers=HEADERS, cookies=COOKIES)
    r.encoding == 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    data = soup.select("tr td")
    Lottery_dates = data[::7]
    issue = data[1::7]
    number = soup.select("tr td em")
    red1 = number[0::7]
    red2 = number[1::7]
    red3 = number[2::7]
    red4 = number[3::7]
    red5 = number[4::7]
    red6 = number[5::7]
    blue1 = number[6::7]

    print("地址:%s 已经分析完毕"% (i))
    for i, j, r1, r2, r3, r4, r5, r6, b1 in zip(Lottery_dates, issue, red1, red2, red3, red4, red5, red6, blue1):
        with open('data.csv', 'a', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [i.string, j.string, r1.string, r2.string, r3.string, r4.string, r5.string, r6.string, b1.string])

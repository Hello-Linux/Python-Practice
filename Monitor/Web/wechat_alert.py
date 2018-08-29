#!/bin/env python3.6
import requests
import json
import re
from bs4 import BeautifulSoup


"""
Define monitor class for baidu
主要功能是根据网站的页面 响应时间 返回状态码 传输过程中本地到网站的网络以及DNS解析有无异常
"""


class Baidu(object):

    def __init__(self, status):
        self.status = status

    def get_token_www(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': 'wxa0cbdeb87c09660c',
                  'corpsecret': '5M0AuphxHzZeXZLI26ffekGXK7iz5Z',
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_token_crm(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': 'wxa0cbdeb87c09660c',
                  'corpsecret': 'RbNPFpDrFSAHqD_TjFHhYOCeg',
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_token_lend(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': 'wxa0cbdeb87c09660c',
                  'corpsecret': 'Ir3uDVwF_gUV2-KtsB_QrJhcb1vC9hQ',
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_msg_www_front(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token_www()
        values = """{"touser" : "wangjun" ,
          "toparty":"2",
          "msgtype":"text",
          "agentid":"1000007",
          "text":{
            "content": "%s"
          },
          "safe":"0"
          }""" % (self.status)
        data = json.loads(values)
        req = requests.post(url, values.encode('utf-8'))

    def send_msg_www_backend(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token_www()
        values = """{"touser" : "wangjun" ,
          "toparty":"2",
          "msgtype":"text",
          "agentid":"1000007",
          "text":{
            "content": "%s"
          },
          "safe":"0"
          }""" % (self.status)
        data = json.loads(values)
        req = requests.post(url, values.encode('utf-8'))

    def send_msg_crm(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token_crm()
        values = """{"touser" : "wangjun" ,
          "toparty":"2",
          "msgtype":"text",
          "agentid":"1000006",
          "text":{
            "content": "%s"
          },
          "safe":"0"
          }""" % (self.status)
        data = json.loads(values)
        req = requests.post(url, values.encode('utf-8'))

    def send_msg_lend(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token_lend()
        values = """{"touser" : "wangjun" ,
          "toparty":"2",
          "msgtype":"text",
          "agentid":"1000008",
          "text":{
            "content": "%s"
          },
          "safe":"0"
          }""" % (self.status)
        data = json.loads(values)
        req = requests.post(url, values.encode('utf-8'))


"""
Alert for baidu
"""
FRONT = requests.get('https://www.baidu.com',
                     allow_redirects=True, timeout=10)
BACKEND = requests.get(
    'http://escrow.baidu.com/login/login.action', allow_redirects=True, timeout=10)
BACKEND_RESPONSE = BACKEND.text
FRONT_RESPONSE = FRONT.text
"""
Get the backend response code
"""
STRING5 = "百度后端网站返回状态码异常"
STRING6 = "百度后端网站网络或者DNS解析异常"
STRING7 = "百度后端网站访问超时"
STRING8 = "百度后端网站页面异常"
HOOMXB_BACKEND5 = Baidu(STRING5)
HOOMXB_BACKEND6 = Baidu(STRING6)
HOOMXB_BACKEND7 = Baidu(STRING7)
HOOMXB_BACKEND8 = Baidu(STRING8)
B_CODE_NUMBER = eval(BACKEND_RESPONSE)['status']

if B_CODE_NUMBER == 1003:
    print("网站访问正常")
else:
    HOOMXB_BACKEND8.send_msg_www_backend()

try:
    if BACKEND.status_code != 200:
        HOOMXB_BACKEND5.send_msg_www_backend()
except requests.ConnectTimeout:
    HOOMXB_BACKEND7.send_msg_www_backend()
except requests.ConnectionError:
    HOOMXB_BACKEND6.send_msg_www_backend()
else:
    print("网站访问正常")


"""
Use Beautifulsoup to get front xml information
"""


STRING1 = "百度前端网站返回状态码异常"
STRING2 = "百度前端网站网络或者DNS解析异常"
STRING3 = "百度前端网站访问超时"
STRING4 = "百度前端网站页面异常"
HOOMXB_FRONT1 = Baidu(STRING1)
HOOMXB_FRONT2 = Baidu(STRING2)
HOOMXB_FRONT3 = Baidu(STRING3)
HOOMXB_FRONT4 = Baidu(STRING4)

soup = BeautifulSoup(FRONT_RESPONSE, "lxml")

CHECK_FRONT = soup.a.string

if CHECK_FRONT == "登录":
    print("网站访问正常")
else:
    HOOMXB_FRONT4.send_msg_www_front()


try:
    if FRONT.status_code != 200:
        HOOMXB_FRONT1.send_msg_www_front()
except requests.ConnectTimeout:
    HOOMXB_FRONT3.send_msg_www_front()
except requests.ConnectionError:
    HOOMXB_FRONT2.send_msg_www_front()
else:
    print("网站访问正常")


"""
Alert for CRM website
"""


CRM = requests.get('https://crm.baidu.com', allow_redirects=True, timeout=10)
response_crm = re.findall(r"crm", CRM.text)

STRING9 = "百度CRM网站返回状态码异常"
STRING10 = "百度CRM网站网络或者DNS解析异常"
STRING11 = "百度CRM网站访问超时"
STRING12 = "百度CRM网站页面异常"
HOOMXB_CRM9 = Baidu(STRING9)
HOOMXB_CRM10 = Baidu(STRING10)
HOOMXB_CRM11 = Baidu(STRING11)
HOOMXB_CRM12 = Baidu(STRING12)
if response_crm[0] == 'crm':
    print("网站访问正常")
else:
    HOOMXB_CRM12.send_msg_crm()

try:
    if CRM.status_code != 200:
        HOOMXB_CRM9.send_msg_crm()
except requests.ConnectTimeout:
    HOOMXB_CRM11.send_msg_crm()
except requests.ConnectionError:
    HOOMXB_CRM10.send_msg_crm()
else:
    print("网站访问正常")


"""
Alert for Lend API
"""

STRING13 = "百度LEND接口返回状态码异常"
STRING14 = "百度LEND接口网络或者DNS解析异常"
STRING15 = "百度LEND接口访问超时"
STRING16 = "百度LEND接口页面异常"
HOOMXB_LEND13 = Baidu(STRING13)
HOOMXB_LEND14 = Baidu(STRING14)
HOOMXB_LEND15 = Baidu(STRING15)
HOOMXB_LEND16 = Baidu(STRING16)

LEND = requests.get('http://lend.baidu.com/lend/test')
response_lend = re.findall(r"SUCCESS", LEND.text)
if response_lend[0] == 'SUCCESS':
    print("网站访问正常")
else:
    HOOMXB_LEND16.send_msg_lend()

try:
    if LEND.status_code != 200:
        HOOMXB_LEND13.send_msg_lend()
except requests.ConnectTimeout:
    HOOMXB_LEND15.send_msg_lend()
except requests.ConnectionError:
    HOOMXB_LEND14.send_msg_lend()
else:
    print("网站访问正常")

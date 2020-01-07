#!/bin/env python
#Date: 2020-1-7
#Author: Sun~shell
#Usage: wget -SO /dev/null http://server_address:server_port/wx/sendMessage?message="your custom message"
import itchat
from flask import Flask, request

itchat.auto_login(enableCmdQR=2,hotReload=True) #the wechat code picture
list = itchat.search_chatrooms(name=u'红上吃饭群')  #we chartroom name
toUserName = list[0]['UserName']

app = Flask(__name__)

@app.route("/wx/sendMessage")
def send_wechat_message():
    '''
    send your custom message to wechat group
    '''
    message = request.args.get('message')
    itchat.send(message, toUserName=toUserName)
    return 'message sent successfully'

#define the listen address and port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888')

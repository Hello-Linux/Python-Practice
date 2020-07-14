# Version:v1.4
# Data: 2020-07-08
# Author: hello_linux@aliyun.com
"""
查看当前启动应用的包名:
u2.connect_wifi().app_current()
彩蛋视频: com.jifen.dandan
快手极速版: com.kuaishou.nebula time:5:30 hours
刷宝短视频: com.jm.video
趣头条: com.jifen.qukan

"""

import os
import time
import subprocess
import threading
import random
import schedule
import tkinter.messagebox
import tkinter as tk
from tkinter import ttk
import uiautomator2 as u2
import weditor

# App线程关闭标志位
stop_threads = True
# 定义全局App线程数组
threads = []
# END


# 扫描以及添加设备
def get_device_all():
    """
    :return: get phone wireless ip devices and connect it
    """
    devices = subprocess.Popen(["adb","devices"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
    devices_new = [x.decode('utf-8') for x in devices.split()]
    serial_nos = []
    for item in devices_new:
        filters = ['list', 'of', 'device', 'devices', 'attached', 'unauthorized', 'offline']
        if item.lower() not in filters:
            serial_nos.append(item)

    wireless_ip = []
    for i in range(len(serial_nos)):
        try:
            # 获取手机IP地址兼容低版本安卓手机
            ip = os.popen('adb -s %s shell "ip address|grep wlan0|grep inet|cut -d\'/\' -f1"' % serial_nos[i]).read().strip().split()[1]
            wireless_ip.append(ip)
        except:
            tkinter.messagebox.showerror('错误', '%s 设备IP地址收集错误!' %(serial_nos[i]))
    with open('phones.csv', 'a+') as file:
        for i in wireless_ip:
            file.write(str(i)+'\n')
    with open('phones.csv', 'r') as device:
        old_devices = device.read().splitlines()
    new_devices = list(set(old_devices))

    with open('phones.csv', 'w') as device:
        for i in new_devices:
            device.write(str(i) + '\n')
    for i in range(len(serial_nos)):
        try:
            print(serial_nos)
            with os.popen('adb -s %s tcpip 5555' % serial_nos[i]):
                time.sleep(5)
            u2.connect_usb("%s" % (serial_nos[i]))
        except:
            print("error")
# END


# 快手极速版
def slide_vertical_kuaishou(start):
    """
    :param start: 定义每个手机设备的索引下标,根据下标执行对应的手机设备
    :return:
    """
    # 点赞数值
    like = 0
    scan_list = []
    with open('phones.csv', 'r') as scan:
        for i in scan.read().splitlines():
            scan_list.append(i)
    devices_address = scan_list
    d = u2.connect_wifi("%s" % (devices_address[start]))
    # 定义弹窗监控器
    d.watcher.when(xpath='//*[@text="设置青少年模式"]').when(xpath='//*[@resource-id="com.kuaishou.nebula:id/button"]/android.widget.LinearLayout[1]').click()
    d.watcher.when(xpath='//*[@text="立即邀请"]').when(xpath='//*[@resource-id="com.kuaishou.nebula:id/close"]').click()
    d.watcher.when(xpath='//*[@text="立即签到"]').click()
    d.watcher.when(xpath="//android.view.View[contains(@text, '签到成功加')]").when(xpath='//*[@resource-id="com.kuaishou.nebula:id/webView"]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[16]/android.view.View[1]/android.view.View[1]').click()
    d.watcher.when(xpath='//*[@text="继续邀好友赚钱"]').when(xpath='//*[@resource-id="com.kuaishou.nebula:id/webView"]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[16]/android.view.View[1]/android.view.View[1]/android.view.View[1]').click()
    d.watcher.when(xpath='//*[@resource-id="com.kuaishou.nebula:id/retry_network_text"]').click()
    d.watcher.start(interval=2.0)
    # END
    d.app_start("com.kuaishou.nebula", stop=True)
    time.sleep(30)

    # 每日签到
    d.xpath('//*[@resource-id="com.kuaishou.nebula:id/left_btn"]').click()
    time.sleep(10)
    d.xpath('//*[@text="去赚钱"]').click()
    time.sleep(15)
    # END

    # 每日福利视频
    d(scrollable=True).scroll.toEnd()
    time.sleep(12)
    if d(text="看精彩视频赚金币").exists:
        for i in range(1,11):
            if d(text="福利").exists:
                d(text="看精彩视频赚金币").right(text="福利").click()
                time.sleep(28)
                d(text="关闭广告").click()
                time.sleep(8)
            else:
                break
    time.sleep(10)
    # END
    # 返回首页看视频
    d.press('back')
    # END
    global stop_threads
    while stop_threads:
        try:
            randomX1 = random.randint(10, 50) + 300
            randomY1 = random.randint(10, 100) + 700
            randomY2 = random.randint(10,100) + 100
            d.swipe(randomX1, randomY1, randomX1, randomY2, 0.1)
            if d(text="点击进入直播间").exists or d.xpath('//*[@resource-id="com.kuaishou.nebula:id/open_long_atlas"]').exists:
                time.sleep(random.randint(1, 2))
            else:
                time.sleep(random.randint(15, 20))
            like += 1
            # 模拟人工点赞
            if like == 35 and not d(text="点击进入直播间").exists:
                d.double_click(randomX1, randomY1)
                like = 0
        except:
            print("%s: 设备模拟出现问题！" % (devices_address[start]))


def slide_vertical_kuaishou_thread():
    try:
        global threads
        scan_list = []
        with open('phones.csv', 'r') as scan:
            for i in scan.read().splitlines():
                scan_list.append(i)
        devices_address = scan_list
        threads = []
        for i in range(len(devices_address)):
            thread = threading.Thread(target=slide_vertical_kuaishou, args=(i,))
            threads.append(thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
    except:
        print("设备线程开启出现问题！")
# END


# 趣头条
def slide_horizontal_qutoutiao(start):
    """
    :param start:
    :return:
    """
    scan_list = []
    with open('phones.csv', 'r') as scan:
        for i in scan.read().splitlines():
            scan_list.append(i)
    devices_address = scan_list
    d = u2.connect_wifi("%s" % (devices_address[start]))
    d.app_start("com.jifen.qukan", stop=True)
    time.sleep(20)
    # 签到
    if d.xpath('//*[@text="去签到"]').exists:
        d.xpath('//*[@text="去签到"]').click_exists()
    time.sleep(10)
    if d(text='恭喜获得'):
        d.xpath('//*[@resource-id="com.jifen.qukan:id/vv"]').click_exists()
    d.xpath('//*[@text="任务"]').click_exists()
    # 进入我的页面
    d.xpath('//*[@text="我的"]').click()
    time.sleep(10)
    # 进入去头条小视频栏目
    d.xpath('//*[@text="小视频"]').click()
    time.sleep(10)
    # END
    global stop_threads
    while stop_threads:
        try:
            # 点击金蛋奖励
            if d.xpath('//*[@resource-id="com.jifen.qukan:id/b0h"]').exists:
                time.sleep(3)
                d.xpath('//*[@resource-id="com.jifen.qukan:id/b0h"]').click()
                time.sleep(3)
                d.xpath('//*[@resource-id="com.jifen.qukan:id/vv"]').click()
            # END
            randomX1 = random.randint(10, 50) + 300
            randomY1 = random.randint(10, 100) + 600
            randomY2 = random.randint(10, 100) + 100
            d.swipe(randomX1, randomY1, randomX1, randomY2)
            time.sleep(random.randint(30,40))
        except:
            print("%s: 设备模拟出现问题！" % (devices_address[start]))


def slide_horizontal_qutoutiao_thread():
    try:
        global threads
        scan_list = []
        with open('phones.csv', 'r') as scan:
            for i in scan.read().splitlines():
                scan_list.append(i)
        devices_address = scan_list
        threads = []
        for i in range(len(devices_address)):
            thread = threading.Thread(target=slide_horizontal_qutoutiao, args=(i,))
            threads.append(thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
    except:
        print("devices is error!")
# END


# 彩蛋视频
def slide_horizontal_caidan(start):
    """
    :param start:
    """
    scan_list = []
    with open('phones.csv', 'r') as scan:
        for i in scan.read().splitlines():
            scan_list.append(i)
    devices_address = scan_list
    d = u2.connect_wifi("%s" % (devices_address[start]))
    d.app_start("com.jifen.dandan", stop=True)
    d.watcher.when(xpath='//*[@text="加载中"]/android.view.View[1]/android.view.View[2]/android.view.View[2]').click()
    d.watcher.start(interval=2.0)
    time.sleep(20)
    # 每日签到
    d(resourceId="com.jifen.dandan:id/image_red_bg_icon").click()
    time.sleep(20)
    if d(textContains="看视频再送").exists:
        d(text="看视频再送100金币").click()
        time.sleep(40)
        d.press("back")
        time.sleep(5)
        d.press("back")
        time.sleep(3)
        d.xpath('//*[@resource-id="com.jifen.dandan:id/tv_close"]').click()
        time.sleep(2)
    # END
    d.press("back")
    global stop_threads
    while stop_threads:
        try:
            if d(text="恭喜您，获得彩蛋奖励! 金币已自动发放至您的钱包").exists:
                d.xpath('//*[@resource-id="com.jifen.dandan:id/close_bottom_button"]').click()
                time.sleep(5)
            randomX1 = random.randint(10, 50) + 300
            randomY1 = random.randint(10, 50) + 600
            randomY2 = random.randint(10, 100) + 100
            d.swipe(randomX1, randomY1, randomX1, randomY2)
            time.sleep(random.randint(15, 25))
        except:
            print("%s: 设备模拟出现问题！" % (devices_address[start]))


def slide_horizontal_caidan_thread():
    try:
        global threads
        scan_list = []
        with open('phones.csv', 'r') as scan:
            for i in scan.read().splitlines():
                scan_list.append(i)
        devices_address = scan_list
        threads = []
        for i in range(len(devices_address)):
            thread = threading.Thread(target=slide_horizontal_caidan, args=(i,))
            threads.append(thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
    except:
        print("设备线程开启出现问题!")
# END


# 刷宝短视频
def slide_horizontal_shuabao(start):
    """
    :param start:
    :param stop:
    :return:
    """
    # 点赞数值
    like = 0
    scan_list = []
    with open('phones.csv', 'r') as scan:
        for i in scan.read().splitlines():
            scan_list.append(i)
    devices_address = scan_list
    d = u2.connect_wifi("%s" % (devices_address[start]))
    d.app_start("com.jm.video", stop=True)
    # 监控器
    d.watcher.when(xpath='//*[@text="去邀请"]').when(xpath='//*[@resource-id="com.jm.video:id/imgClose"]').click()
    d.watcher.start(2.0)
    time.sleep(15)
    global stop_threads
    while stop_threads:
        try:
            randomX1 = random.randint(10, 50) + 300
            randomY1 = random.randint(10, 100) + 600
            randomY2 = random.randint(10, 100) + 100
            d.swipe(randomX1, randomY1, randomX1, randomY2)
            if d.xpath('//*[@resource-id="com.jm.video:id/textViewGoLiveFromVideoPop"]').exists:
                time.sleep(random.randint(1, 2))
            else:
                time.sleep(random.randint(15, 25))
            like += 1
            # 模拟人工点赞
            if like == 20:
                d.double_click(randomX1, randomY1)
                like = 0
        except:
            print("%s: 设备模拟出现问题！" % (devices_address[start]))


def slide_horizontal_shuabao_thread():
    try:
        global threads
        scan_list = []
        with open('phones.csv', 'r') as scan:
            for i in scan.read().splitlines():
                scan_list.append(i)
        devices_address = scan_list
        threads = []
        for i in range(len(devices_address)):
            thread = threading.Thread(target=slide_horizontal_shuabao, args=(i,))
            threads.append(thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
    except:
        print("设备线程出现问题！")
# END


# END
# 定义Ａpp关闭函数
def stop_video(app_name):
    scan_list = []
    with open('phones.csv', 'r') as scan:
        for i in scan.read().splitlines():
            scan_list.append(i)
    global stop_threads
    stop_threads = False
    devices_address = scan_list
    for i in range(len(devices_address)):
        u2.connect_wifi("%s" % (devices_address[i])).watcher.reset()
        u2.connect_wifi("%s" % (devices_address[i])).app_stop(app_name)
        time.sleep(5)
    for t1 in threads:
        t1.join()

window = tk.Tk()
window.title('群控系统V1.0.0')

# 获取当前屏幕长宽
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
# 设定窗口的大小(长 * 宽)
width = 500
height = 700
size = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
window.geometry(size)
window.resizable(0, 0)

b1 = tk.Button(window,
    text='快手极速',
    width=8,
    height=1,
    activebackground='green',
    bg='grey',
    font=('微软雅黑',10,'bold'),
    fg='yellow',
    command=slide_vertical_kuaishou_thread)
b1.place(x=80,y=100,anchor='nw')

b2 = tk.Button(window,
    text='刷宝短视频',
    width=8,
    height=1,
    activebackground='green',
    bg='grey',
    font=('微软雅黑',10,'bold'),
    fg='yellow',
    command=slide_horizontal_shuabao_thread)
b2.place(x=160,y=100,anchor='nw')

b3 = tk.Button(window,
    text='趣头条',
    width=8,
    height=1,
    activebackground='green',
    bg='grey',
    font=('微软雅黑',10,'bold'),
    fg='yellow',
    command=slide_horizontal_qutoutiao_thread)
b3.place(x=240,y=100,anchor='nw')

b4 = tk.Button(window,
    text='彩蛋视频',
    width=8,
    height=1,
    activebackground='green',
    bg='grey',
    font=('微软雅黑',10,'bold'),
    fg='yellow',
    command=slide_horizontal_caidan_thread)
b4.place(x=0,y=150,anchor='nw')
columns = ("number", "factory", "model")
style = ttk.Style(window)
style.theme_use("clam")
style.configure("Treeview", font=('微软雅黑',9,'bold'), rowheight=20, background="black", foreground="DarkOrange", fieldbackground="black")
tree = ttk.Treeview(window, show="headings", columns=columns,height=15)
tree.column("number", anchor="center",width=50)
tree.column("factory", anchor="center",width=50)
tree.column("model", anchor="center",width=50)
tree.heading("number", text="设备编号")
tree.heading("factory", text="手机厂商")
tree.heading("model", text="手机型号")
tree.pack(side='bottom', fill='x')


# 设备打印
def scan_devices():
    tree.tag_configure('gray', background='yellow')
    scan_list = []
    with open('phones.csv', 'r') as scan:
        for i in scan.read().splitlines():
            scan_list.append(i)
    old_device = tree.get_children()
    for item in old_device:
        tree.delete(item)
    j = 0
    for i in range(len(scan_list)):
         j += 1
         if (j & 1) == 0:
             tree.insert('', j, values=(j, u2.connect_wifi("%s" % (scan_list[i])).shell("getprop ro.product.brand")[0], u2.connect_wifi("%s" % (scan_list[i])).shell("getprop ro.product.model", timeout=30)[0]))
         else:
             tree.insert('', j, values=(j, u2.connect_wifi("%s" % (scan_list[i])).shell("getprop ro.product.brand")[0], u2.connect_wifi("%s" % (scan_list[i])).shell("getprop ro.product.model", timeout=30)[0]), tag='gray')

b6 = tk.Button(window,
    text='添加设备',
    width=10,
    height=2,
    activebackground='blue',
    bg='grey',
    bd=3,
    font=('微软雅黑',10,'bold'),
    fg='yellow',
    command=get_device_all)
b6.place(x=0,y=0,anchor='nw')

b7 = tk.Button(window,
    text='打印设备',
    width=10,
    height=2,
    activebackground='blue',
    bg='grey',
    bd=2,
    font=('微软雅黑',10,'bold'),
    fg='yellow',
    command=scan_devices)
b7.place(x=200,y=0,anchor='nw')
# 定时执行群控系统APP
# schedule.every().day.at("06:43:30").do(slide_vertical_kuaishou_thread)
# schedule.every().day.at("12:00:00").do(stop_video, "com.kuaishou.nebula")
# schedule.every().day.at("12:00:30").do(slide_horizontal_caidan_thread)
# schedule.every().day.at("13:30:00").do(stop_video, "com.jifen.dandan")
# schedule.every().day.at("13:30:30").do(slide_horizontal_shuabao_thread)
# schedule.every().day.at("17:30:00").do(stop_video, "com.jm.video")
# schedule.every().day.at("17:30:30").do(slide_horizontal_qutoutiao_thread)
# schedule.every().day.at("21:00:00").do(stop_video, "com.jifen.qukan")

# 定时执行扫描设备函数
schedule.every(60).seconds.do(scan_devices)
# END

# Tkinker 定义轮询schedule任务
def my_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
thread1 = threading.Thread(target=my_schedule)
thread1.daemon = True
thread1.start()
# END
window.mainloop()

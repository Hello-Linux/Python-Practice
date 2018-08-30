#!/bin/env python3.7

'''
This python program is mainly used to clear table space
'''
import pymysql

db = pymysql.connect(host='192.168.1.30', port=3306, user='root', passwd='password', db='information_schema')

cursor = db.cursor()

cursor.execute("select concat(table_schema,'.',table_name) from information_schema.tables where table_schema not in (\"information_schema\", \"mysql\") and data_free > 0;")
result = cursor.fetchall()
for t in range(len(result)):
    print("正在清理 %s 表空间" % (result[t]))
    cursor.execute("optimize table %s" %(result[t]))
db.commit()
cursor.close()
db.close()

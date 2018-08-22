#!/bin/env python3.7

'''
This python program is mainly used to modify the database time fields for each test environment
'''
import paramiko
import pymysql
HOSTNAME = ['192.168.1.26', '192.168.1.27', '192.168.1.28', '192.168.1.29', '192.168.1.31',
            '192.168.1.32', '192.168.1.34', '192.168.1.35', '192.168.1.36', '192.168.1.37']
DB_LIST = ['hoomxb26', 'hoomxb27', 'hoomxb28', 'hoomxb29', 'hoomxb31',
           'hoomxb32', 'hoomxb34', 'hoomxb35', 'hoomxb36', 'hoomxb37']

PORT = 22
USERNAME = 'root'
PRIVATE_KEY = paramiko.RSAKey.from_private_key_file("/opt/id_rsa")
TIME_LIST = []

for index1, data in enumerate(HOSTNAME):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=HOSTNAME[index1], port=PORT,
                username=USERNAME, pkey=PRIVATE_KEY)
    stdin, stdout, stderr = ssh.exec_command('date "+%Y-%m-%d %H:%M.%S"')
    result = stdout.read().decode()
    ssh.close()
    TIME_LIST.append(result)


def change_time():
    ''' change database time for every enumerate time '''
    for index2, data in enumerate(DB_LIST):
        try:
            connection = pymysql.connect(
                host='192.168.1.30', port=3306, user='root', passwd='password', db=DB_LIST[index2])
            with connection.cursor() as cursor:
                cursor.execute(
                    "update server_time set time_ = %s", (TIME_LIST[index2]))
            connection.commit()
        except ConnectionError:
            print("Your database cant't connect!!")
        finally:
            connection.close()


if __name__ == "__main__":
    change_time()

#!/bin/env python
import os
import sys
from datetime import timedelta, datetime
from ftplib import FTP
host = '1.2.3.4'
username = 'xxxxxxxxx'
password = 'xxxxxxx'

yesterday = datetime.today() + timedelta(-1)
yesterday_format = yesterday.strftime('%Y%m%d')


class FTPSync(object):
    def __init__(self):
        self.conn = FTP()
        self.conn.connect(host, 20022, 60)
        self.conn.login(username, password)
        self.conn.cwd('%s'%(yesterday_format))
        if not os.path.exists('/upload/check/%s'%(yesterday_format)):
            os.mkdir('/upload/check/%s'%(yesterday_format))
        os.chdir('/upload/check/%s'%(yesterday_format))

    def get_dirs_files(self):
        dir_res = []
        self.conn.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return files, dirs

    def walk(self, next_dir):
        sys.stderr.write('Walking to %s\n'%next_dir)
        self.conn.cwd(next_dir)
        try:
            os.mkdir(next_dir)
        except OSError:
            pass
        os.chdir(next_dir)
        ftp_curr_dir = self.conn.pwd()
        local_curr_dir = os.getcwd()
        files, dirs = self.get_dirs_files()
        sys.stdout.write("FILES: %s"%files)
        sys.stdout.write("DIRS: %s"%dirs)
        for f in files:
            if not os.path.exists('/upload/check/%s/%s'%(yesterday_format,f)):
                sys.stdout.write("%s : %s"%(next_dir, f))
                sys.stdout.write("download : %s"%os.path.abspath(f))
                outf = open(f, "wb")
                try:
                    self.conn.retrbinary("RETR %s"%f, outf.write)
                finally:
                    outf.close()
        for d in dirs:
            os.chdir(local_curr_dir)
            self.conn.cwd(ftp_curr_dir)
            self.walk(d)

    def run(self):
        self.walk('.')

def main():
    f = FTPSync()
    f.run()


if __name__ == '__main__':
    main()

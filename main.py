# -*-coding:utf=8 -*-
'''
======================================
author:jxy
lang:python
mail:czjxy8898@gmail.com
university:China,Xidian University
**If you need to reprint,please indicate the source**
======================================
'''


import renren
import sql
from remind import *
import datetime
import os
import threading
import random
import sys
import logging
import ctypes
import time


def error():
    global tee
    t = 0
    while 1:
        time.sleep(0.1)
        t += 0.3
        if t > 10:
            break
    # os.execl('python','python',*sys.argv)
    ctypes.pythonapi.PyThreadState_SetAsyncExc(tee.ident, ctypes.py_object(tee))
    os.system("python main.py")
    exit()


def respond():
   # try:
    t = 1
    ren = renren.Renren(account[0], account[1], account[2])
    while 1:
        ren.check()
        tt = ren.getNotifications()
        i = 0
        # print len(tt)
        while i != len(tt):
            ren.Respond(tt[i])
            i += 1
        if i == 0:
            if t < 120:
                t += 1
        if i != 0:
            if t > 5:
                t = 5
            elif t >= 1:
                t -= 1
        time.sleep(t)
        print "respond time %d %d " % (t, len(tt))
   # except Exception,e:
   # print e
   # tee=threading.Thread(target=respond)
   # tee.setDaemon(True)
   # tee.start()


def que(m):
    if 0 <= m < 6:
        return '格言欣赏:' + meng.poem()
    elif 5 < m < 8:
        return meng.find('天气')
    elif m == 8 or m == 13:
        return meng.find('国内')
    elif m == 9 or m == 11 or m == 22:
        return meng.find('NBA')
    elif m == 12 or m == 16 or m == 23:
        return meng.find('趣闻')
    elif m == 10 or m == 21:
        return meng.find('军事')
    elif m == 14:
        return meng.find('娱乐')
    elif m == 15:
        return meng.find('音乐')
    elif m == 17:
        return meng.find('Cnbeta')
    elif m == 18:
        return meng.find('要闻')
    elif m == 19:
        return meng.find('教务处')
    elif m == 20:
        return meng.find('环球')


def tt():
    ren = renren.Renren(account[0], account[1], account[2])
    while 1:
        ren.check()
        rem = remind()
        t = time.localtime()
        try:
            if meng.update() == 0:
                meng.update()
        except:
            meng.update()
        try:
            ss = que(t.tm_hour)
        except:
            ss = "塔塔累了，休息一下"

        while 1:
            t = time.localtime()
            if t.tm_min == 0:
                break
            time.sleep(1)
        content = '塔塔报时:现在时间  '+time.strftime('%Y-%m-%d %H:%M:00', t)+"  "
        content = (content+'   '+rem)+ss
        ren.publish(content)
        time.sleep(1800)
        if random.randint(0, 10) == 0:
            ren.check()
            d = ren.getrecentcomment()
            if d < 24:
                s = meng.sad()
            elif d > 48:
                s = meng.well()
            else:
                s = ""
            if s != "":
                ren.publish(s)
        time.sleep(1600)


if __name__ == '__main__':
    account = []
    if len(sys.argv) == 1:
        accountFile = open('account/xdutower.txt', 'r')
        for i in range(0, 3):
            account.append(accountFile.readline().strip())
    elif sys.argv[1] == 'debug':
        accountFile = open('account/xiaoxiaoxdu.txt', 'r')
        for i in range(0, 3):
            account.append(accountFile.readline().strip())
    else:
        print('Error Args')
        exit(1)
    logger = logging.getLogger()
    handler = logging.FileHandler("main.log")
    formatter = logging.Formatter('%(asctime)s %(lineno)d  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)

    meng = sql.Sql()
    tee = threading.Thread(target=respond)
    tee.setDaemon(True)
    tee.start()
    tt()
    # except Exception,e:
    #    logger.error(e)
    #    error()

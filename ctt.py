# -*- coding: utf-8 -*-
import os,time,subprocess,httplib
'''
同步时间
'''
def changetime(t):
   l=time.localtime(t)
   dat="date %u-%02u-%02u"%(l.tm_year,l.tm_mon,l.tm_mday)
   tm="time %02u:%02u:%02u"%(l.tm_hour,l.tm_min,l.tm_sec)
   subprocess.Popen(dat, shell=True)
   subprocess.Popen(tm, shell=True)
   return 1

def change():
    t=time.time()
    while 1:
        t+=60
        changetime(t)
        time.sleep(30)

def getBeijinTime():
     try:
         conn = httplib.HTTPConnection("www.beijing-time.org")
         conn.request("GET", "/time.asp")
         response = conn.getresponse()
         if response.status == 200:
             #解析响应的消息
             result = response.read()
             data = result.split("\r\n")
             year = data[1][len("nyear")+1 : len(data[1])-1]
             month = data[2][len("nmonth")+1 : len(data[2])-1]
             day = data[3][len("nday")+1 : len(data[3])-1]
             #wday = data[4][len("nwday")+1 : len(data[4])-1]
             hrs = data[5][len("nhrs")+1 : len(data[5])-1]
             minute = data[6][len("nmin")+1 : len(data[6])-1]
             sec = data[7][len("nsec")+1 : len(data[7])-1]
             
             beijinTimeStr = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
             beijinTime = time.strptime(beijinTimeStr, "%Y/%m/%d %X")
             return time.mktime(beijinTime) 
     except:
         return None

def uptime():
   t=getBeijinTime()
   if t==None:return 0
   return changetime(t)


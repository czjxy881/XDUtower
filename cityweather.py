# -*- coding:utf=8 -*_
import urllib
import urllib2
import re
import sys


def findname(encoded_args):
    for i in range(10):
        try:
            response = urllib2.urlopen('http://tianqi.2345.com/t/q.php', encoded_args)
            regs = re.compile(r'2345天气预报最新提示，(.+)（分享自 @2345天气预报）'.decode('utf-8').encode('gb2312'))
            result = regs.findall(response.read())
            # print result
            return result[0].decode('gb2312', 'ignore').encode('utf-8')
        except IndexError:
            continue

    return findurl(raw_citycode, encoded_args)


def findurl(raw_citycode, encoded_args):
    #print "ok"
    for i in range(1000):
        try:
            response = urllib2.urlopen('http://tianqi.2345.com/t/q.php', encoded_args)
            reg = r'<dl><dt><a href="(\S+)" title="%s天气预报">' % raw_citycode
            regs = re.compile(reg.decode('utf-8').encode('gb2312'))
            new_url = regs.findall(response.read())
            break
        except IndexError:
            continue
    #print new_url
    my_header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'UTF-8,*;q=0.5',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22'
    }
    for i in range(1000):
        try:
            request = urllib2.Request(url='http://tianqi.2345.com' + new_url[0].decode('gb2312', 'ignore').encode('utf-8'), headers=my_header)
            response = urllib2.urlopen(request)
            #f = open('k.html','w')
            #f.write(response.read())
            regs = re.compile(r'2345天气预报最新提示，(.+)（分享自 @2345天气预报）'.decode('utf-8').encode('gbk'))
            result = regs.findall(response.read())
            return result[0].decode('gbk', 'ignore').encode('utf-8')
        except IndexError:
            continue
    return "查询失败"


def findcity(name):
    global raw_citycode
    raw_citycode = name
    citycode = raw_citycode.decode('utf-8').encode('gb2312')
    tianqi_args = {'city': citycode}
    encoded_args = urllib.urlencode(tianqi_args)
    return findname(encoded_args)

if __name__ == "__main__":
   name = sys.argv[1]
   print findcity(name)
   #f = open('k.html', 'r')
   #regs = re.compile(r'2345天气预报最新提示，(.+)（分享自 @2345天气预报）'.decode('utf-8').encode('gbk'))
   #result = regs.findall(f.read())
   #print result[0].decode('gbk', 'ignore').encode('utf-8')

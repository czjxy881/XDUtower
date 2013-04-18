
#-*- coding: utf-8 -*-
import feedparser
import sys
import re
import urllib
import time


class Rili:

    def a(self):
        page = urllib.urlopen('http://www.nongli.com/item4/index.asp')
        html = page.read()
        # print html
        reg = r'<td width="74%" bgcolor="#FFFFFF"><B>(.*?)</B></td>'
        a = re.compile(reg)
        b = a.findall(html)
        return b

    def c(self, co, n):
        a = re.sub('\s+', ',', co)
        return n+a.decode('cp936').encode('utf-8')

    def b(self):
        name = ['农历:', ';干支：', ';适宜：', ';忌讳:']
        aa = self.a()
        ans = ''
        for i in range(0, 4):
            if ''.join(aa[i].split()) == '':
                ans += name[i]+'无'
            else:
                ans += self.c(aa[i], name[i])
        return ans


class message:

    def c(self, s):
        s = s.title.encode('utf-8')
        s = s.replace(' ', '')
        s = re.sub(r'<.*?br.*?>', '-', s)
        s = re.sub('(图)', '', s)
        s = re.sub('（视频）', '', s)
        return s

    def geturl(self, urll):
        a = feedparser.parse(urll)
        a0 = self.c(a.entries[0])+';'
        a1 = self.c(a.entries[1])+';'
        a2 = self.c(a.entries[2])+';'
        aa = a0+a1+a2
        return aa

    def getHtml(self, url):
        page = urllib.urlopen(url)
        html = page.read()
        page.close()
        return html

    def weather(self):
        # 获取天气
        def getWeather(html):
            reg = '天气提醒，(.*?)（'.decode('utf-8').encode('cp936')
            weatherList = re.compile(reg).findall(html)
            return weatherList
        return (getWeather(self.getHtml('http://xian.tianqi.com/changan/'))[0]).decode('cp936').encode('utf-8')

    def basketball(self):
        # 获取篮球新闻
        def getscore(html):
            reg = '<a target="_blank" onclick=.*? title=.*?>(.*?)</a>(.|\n)*?<a target=.*? href =.*?>\s*(.*?)\s*</a>(.|\n)*?<a target="_blank" onclick=.*? title=.*?>(.*?)</a>(.|\n)*?<a href=.*? onclick=.*? target=.*? title=.*?>(.*?)</a>'
            reg1 = '<a target="_blank" onclick=.*? title=.*?>(.*?)</a>(.|\n)*?<span class="bifen">\s*(.*?)\s*</span>(.|\n)*?<a target="_blank" onclick=.*? title=.*?>(.*?)</a>(.|\n)*?<a href=.*? onclick=.*? target=.*? title=.*?>(.*?)</a>'
            score = re.compile(reg).findall(html)
            score += re.compile(reg1).findall(html)
            return score

        def chinese(s):
            return len(s) == len(unicode(s, 'gb2312'))
        a = getscore(self.getHtml('http://www.hoopchina.com'))
        s = ''
        now = 0
        for i in range(len(a)):
            if chinese(a[i][2]):
                if now <= 2:
                    for j in range(len(a[i])):
                        if a[i][j] != ' 'or j == 5:
                            s = s+a[i][j].decode('cp936').encode('utf-8')
                    s = s+'; '
                now += 1
        if now == 0:
            return "今天没有NBA o(︶︿︶)o  "
        return ("NBA时报：今天共%d场比赛," % now+s)
    # 获取教务处新闻

    def jwcnews(self):
        t = time.localtime()
        url = 'http://jwc.xidian.edu.cn'

        def getnews(html):
            reg = '\[ (\d\d\d\d)-(\d\d)-(\d\d) \] <A href=(.*?) .*?>(.*?)</'
            news = re.compile(reg).findall(html)
            reg1 = '<script src=\"(.*?)\">'
            b = re.compile(reg1).findall(html)
            for j in range(len(b)):
                hh = self.getHtml(b[j])
                c = re.compile(reg).findall(hh)
                news += c
            return news
        a = getnews(self.getHtml(url))
        s = ''
        j = 0
        for i in range(len(a)):
            if a[i][0] == str(t.tm_year) and a[i][1] == '%02d' % t.tm_mon and a[i][2] == '%02d' % t.tm_mday:
            # 当日通知
                m = a[i][3]
                m = m.replace('"', '')
                s = s+a[i][4]+",详情见："+url+m+" ;"
                j += 1
                if j > 2:
                    s += '今日还有更多通知，请见教务处'
                    break
        if s == '':
            return '今日教务处无新通知'
        else:
            return ("校内通知： "+s)

    #Cnbeta News
    def cnbetanews(self):
        cb = self.getHtml('http://www.cnbeta.com')
        reg = r'<dt class="topic" ><a href=".+"  target="_blank"><strong>(.+)</strong></a></dt>'
        result = re.compile(reg).findall(cb)
        a = 'Cnbeta新闻:'
        for item in result[0: 3]:
            item = item.decode('GBK').encode('utf-8')
            a += item + ';'
        a += '详情见:http://www.cnbeta.com'
        return a
        
    def getmsg(self, message):
        if message == 1:
            urll = 'http://news.sohu.com/rss/guonei.xml'
            a = self.geturl(urll)
            return '国内新闻：'+a+'详情见:http://news.sohu.com/1/0903/60/subject212846065.shtml'
        if message == 2:
            urll = 'http://cn.engadget.com/rss.xml'
            a = self.geturl(urll)
            return '科技趣闻：'+a+'详情见:http://cn.engadget.com/'
        if message == 3:
            urll = 'http://news.baidu.com/n?cmd=4&class=shizheng&tn=rss'
            a = self.geturl(urll)
            return '环球视野:'+a+'详情见:http://news.baidu.com/n?cmd=4&class=hqsy&t'
        if message == 4:
            urll = 'http://rss.sina.com.cn/roll/mil/hot_roll.xml'
            a = self.geturl(urll)
            return '军事汇总：'+a+'详情见:http://news.sina.com.cn/news1000/index.shtml?requestOrder=3'
        if message == 5:
            urll = 'http://rss.sina.com.cn/ent/hot_roll.xml'
            a = self.geturl(urll)
            return '娱乐八卦：'+a+'详情见:http://news.sina.com.cn/news1000/index.shtml?requestOrder=5'
        if message == 6:
            urll = 'http://rss.sina.com.cn/ent/music/focus12.xml'
            a = self.geturl(urll)
            return '音乐资讯：'+a+'详情见:http://ent.sina.com.cn/y/news.html'
        if message == 7:
            urll = 'http://rss.sina.com.cn/tech/rollnews.xml'
            a = self.geturl(urll)
            return '科技要闻：'+a+'详情见:http://tech.sina.com.cn/roll.shtml'
        if message == 8:
            return self.weather()
        if message == 9:
            w = Rili()
            return w.b()
        if message == 10:
            return self.basketball()
        if message == 11:
            return self.jwcnews()
        if message == 12:
            return self.cnbetanews()

if __name__ == '__main__':

    a = message()
    for i in range(1, 13):
        print a.getmsg(i)

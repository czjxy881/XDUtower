# coding:utf-8
import requests
import urllib
import re
import sql
import random


class Xhj:

    def __init__(self):
        self.session = requests.session()
        self.chat_url = 'http://www.simsimi.com/func/req?lc=ch&msg='
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.4) Gecko/20100611 Firefox/3.6.4 ( .NET CLR 3.5.30729; .NET4.0C)'        ,'Accept':'application/json, text/javascript, */*; q=0.01'
        ,'Accept-Language':'zh-CN,zh;q=0.8'
        ,'Accept-Encoding':'gzip,deflate,sdch'
        ,'Content-Type':'application/json; charset=utf-8'
        ,'X-Requested-With':'XMLHttpRequest'
        ,'Referer':'http://www.simsimi.com/talk.htm?lc=ch'
        ,'host':'www.simsimi.com'
        ,'Connection':'keep-alive'})
        self.session.get('http://www.simsimi.com/talk.htm')
        self.s = sql.Sql()

    def chat(self, mes):
      #  print mes,type(mes)
        if isinstance(mes, str):
            mes = mes.decode('GBK')
       # print type(mes),isinstance(mes,str)
        mes = re.sub(u'<.*?>', '', mes)
        l = mes.find(u'@')
        # print mes
        while l != -1:
            r = mes.find(u')', l)
            if r == -1:
                r = mes.find('>', l)
            if r == -1:
                r = l-1
            mes = mes[:l]+mes[r+2:]
            l = mes.find(u'@')
        mes = u''.join(mes.split())
        if mes.find(u'：') != -1:
            mes = mes[mes.find(u'：')+1:]
        if mes.find(u':') != -1:
            mes = mes[mes.find(u':')+1:]
        mes = re.sub(u'塔塔', u'小黄鸡', mes)
        # print mes
        if mes == "":
            mes = u'hi'
       # print mes
        r = self.session.get(self.chat_url+urllib.quote(mes.encode('utf-8')))
        result = r.json()
       # print result
        if result.has_key(u'id') and result[u'id'] != 1:
            if re.search(u'微\s*信', result[u'response']) == None and re.search(u'@', result[u'response']) == None:
                result[u'response'] = re.sub(u'小*.*鸡', u'塔塔', result[u'response'])
                return result[u'response'].encode('utf-8')
        return self.s.no()

if __name__ == '__main__':

    xiaohuangji = Xhj()
    print xiaohuangji.chat(u"\u80bf\u4e48\u53ef\u4ee5\u8fd9\u6837<img src='http://a.xnimg.cn/imgpro/icons/statusface/yali.gif' alt='\u9e2d\u68a8'/>").decode('utf-8').encode('GBK')
    while 1:
        s = raw_input('me:')
       # print re.search(u'微\s*信',s.decode('GBK'))
        print 'Huang:'+xiaohuangji.chat(s).decode('utf-8').encode('GBK')

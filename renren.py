
#code:utf-8
'''
Created on 2013-4-12

@author: jxy
'''
import os,urllib2,urllib,cookielib,random,requests,re,json,logging
import xhj,time,jieba,sql
class Renren():
    '''
    用于模拟各种人人api
    版权所有：czjxy881
    Email：czjxy8898@gmail.com
    '''
    def __init__(self,email='',password='',pid=''):
        #设置log文件
        self.logger=logging.getLogger()
        handler=logging.FileHandler("renren.log")
        formatter = logging.Formatter('%(asctime)s %(lineno)d  %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)
        self.email=email;
        self.password=password;
        self.session=requests.session();
        self.session.headers.update({'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.4) Gecko/20100611 Firefox/3.6.4 ( .NET CLR 3.5.30729; .NET4.0C)'
                                 #    ,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                                 #    ,'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
                                  #   ,'Accept-Encoding':'gzip, deflate'
                                  #   ,'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
                                   #  ,'X-Requested-With':'XMLHttpRequest'
                                   #  ,'Referer':'  http://www.renren.com/'
                                     ,'Connection':'keep-alive'})
        self.token = {}
        self.data=[]
        self.pid=pid
        self.cookie='cookie_'+self.pid
        self.sq=sql.Sql()
        self.hj=0
    #直接登录
    def login(self): 
        self.session.cookies=requests.session().cookies
        self.session.get('http://www.renren.com/')
        fn = 'icode%s.jpg' % os.getpid()
        self.geticode(fn)
        if self.getShowCaptcha(self.email) == 1:
            os.system(fn)
            icode = raw_input().strip()
        else:
            icode = ''
        os.remove(fn)
        data = {
            'email': self.email,
            'icode': icode,
            'domain': 'renren.com',
            'password':self.password,
            'autoLogin':'true',
        }
        print "start login"
        url = 'http://www.renren.com/ajaxLogin/login'
        #print url; 
        r = self.session.post(url, data)
        result = r.json()
        if result['code']:
            #print result['homeUrl']
            r = self.session.get(result['homeUrl'])
            f=0
            while self.getToken(r.text)==0:
                f+=1
                if f>3:raise
            self.saveCookie(self.cookie)
            print 'login successfully'
        else:
            print 'login error', r.text
    #获取认证      
    def getToken(self, html=''):
        p = re.compile("get_check:'(.*)',get_check_x:'(.*)',env")

        if not html:
            r = self.session.get('http://www.renren.com')
            html = r.text
        try:
            result = p.search(html)
            self.token = {
                          'requestToken': result.group(1),
                          '_rtk': result.group(2)
                          }
            return 1
        except Exception,e:
             print Exception,e
             self.logger.error(e)
             return 0
    #获取验证码
    def geticode(self,fn):
        r = self.session.get("http://icode.renren.com/getcode.do?t=web_login&rnd=%s" % random.random())
        if r.status_code == 200 and r.raw.headers['content-type'] == 'image/jpeg':
            with open(fn, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
    #检测是否需要输入验证码                
    def getShowCaptcha(self, email=None):
        r = self.session.post('http://www.renren.com/ajax/ShowCaptcha', data={'email': email})
        return r.json()
    #保存cookie
    def saveCookie(self,cookie_path):
        with open(cookie_path, 'w') as fp:
            cookie_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
            cookie_str = '; '.join([k + '=' + v for k, v in cookie_dict.iteritems()])
            fp.write(cookie_str)
    #从cookie登录      
    def loginByCookie(self, cookie_path):
       try:
        print 'Cookie login begin'
        with open(cookie_path) as fp:
            cookie_str = fp.read()
        cookie_dict = dict([v.split('=', 1) for v in cookie_str.strip().split('; ')])
        self.session.cookies = requests.utils.cookiejar_from_dict(cookie_dict)
        self.session.cookies['t']=self.session.cookies['societyguester']
        #校验码同步，非常重要
        f=0
        while self.getToken()==0:
            f+=1
            if f>3:raise
        print 'success'
       except Exception,e:
         print Exception,e
         self.logger.error(e)
         print 'error'
    #获取个人信息
    def getInfo(self):
      try:
        r=self.session.get('http://notify.renren.com/wpi/getonlinecount.do')
        try:
            self.data=r.json()
        except:
            self.data=[]
        return 1
      except:
        return 0
    #检测当前登录状态
    def check(self):
        self.data=[]
        if self.getInfo()==0:self.getInfo()
        if  self.data==[]:self.loginByCookie(self.cookie)
        else :return 1
        if self.getInfo()==0:self.getInfo()
        if self.data==[]:self.login()
        else:return 1
        if self.getInfo()==0:self.getInfo()
        if self.data==[]:return 0
        else: return 1
    #获取uid的一页状态
    def  getDoings(self,uid,page):
        url='http://status.renren.com/status/someone?userId=%s&curpage=%s'%(uid,page)
        r=self.session.get(url)
        return r.json().get('doingArray',[])
    #获取通知
    def getNotifications(self): 
        url = 'http://notify.renren.com/rmessage/get?getbybigtype=1&bigtype=1&limit=50&begin=0&view=17'
        r = self.session.get(url)
        v=r.text
        #print v
        v=re.sub(r'(:)(\w*)([,}])',r'\1"\2"\3',v) #change to json
        try:
            result = json.loads(v, strict=False)
        except Exception, e:
            print Exception,e
            self.logger.error(e)
            raise
            result = []
        return result
    #删除通知
    def removeNotification(self, notify_id,tp):
        return self.session.get('http://notify.renren.com/rmessage/remove?nl=%s&uid=%s&type=%s'%(str(notify_id),self.pid,tp))
    
    def send(self,url,data):
        data.update(self.token)
        try:
            r=self.session.post(url,data=data)
           # print r.text
            x=r.json()
            if (x.has_key('type') and x['type']==6) or x.has_key('replyList'):return x
            elif x.has_key('code') and x['code']==0:
                return 1
            else:
                print 'error:'+x['msg']
                return 0
        except Exception,e:
            print Exception,e
            self.logger.error(e)      
            return 0
    #获得一篇评论  
    def getDoingComments(self, owner_id, doing_id,t):
        url = 'http://status.renren.com/feedcommentretrieve.do'
        r = self.send(url,{
            'doingId': doing_id,
            'source': doing_id,
            'owner': owner_id,
            't':t
        })
       # print r
        return r['replyList']
    #获得一条评论
    def getCommentById(self, owner_id, doing_id, comment_id,t):
        comments = self.getDoingComments(owner_id, doing_id,t)
        comment = filter(lambda comment: comment['id'] == int(comment_id), comments)
        return comment[0] if comment else None
    
    #发表公共主页状态
    def publish(self,content):
        # url='http://shell.renren.com/'+str(self.data['hostid'])+'/status'
        url='http://page.renren.com/doing/update'
        '''#这个是个人的
        d={'content':content,
              'hostid':str(self.data['hostid']),
              'channel':'renren'
              }
        '''
        d={
           'c':content,
           'asMobile':0,
           'cid':0,
           'gid':0,
           'pid':self.pid
           }
        return self.send(url,d)
    #回复状态
    def addStatuesComment(self,content,data):
        url='http://status.renren.com/feedcommentreply.do'
        #url='http://page.renren.com/doing/reply'
        d={
           't': 3,
           'rpLayer': 0,
           'c':content,
           'owner':data['owner'],
           'source':data['source'],
           }
        #print content
        if data.get('replied_id', None):
            d.update({
                'rpLayer': 1,
                'replyTo': data['from'],
                'replyName': data['from_name'],
                'secondaryReplyId': data['replied_id'],
                'c': '回复%s:%s' % (data['from_name'].encode('utf-8'), content)
            })
        return self.send(url,d)
    def addSharein(self):
        url='http://share.renren.com/share/submit.do'
        post='''{"sendcomment"=true,

                }'''



    
    #添加分享外网
    def addShare(self,link,comment):
        url='http://shell.renren.com/'+self.pid+'/url/parse'
        d={
             'comment':comment,
             'link':link,
             'hostid':self.pid
           }
        d=self.send(url,d)
        d.update({
                  'hostid':self.pid,
                  'channel':'renren',
                  'nothumb':'off',
                  'comment':comment
        })
        url='http://shell.renren.com/'+self.pid+'/share?1'
        #print d
        self.send(url,d)
    #评论分享
    def addShareComment(self,comment,data):
        url='http://status.renren.com/feedcommentreply.do?ft=share'
        d={
           't': 4,
           'rpLayer': 0,
           'c':comment,
           'owner':data['owner'],
           'source':data['source'],
           }
        if data.get('replied_id', None):
            d.update({
                'rpLayer': 1,
                'replyTo': data['from'],
                'replyName': data['from_name'],
                'secondaryReplyId': data['replied_id'],
                'c': 'reply %s:%s' % (data['from_name'].encode('utf-8'), comment)
            })
        return self.send(url,d)
    #添加留言（主页未测试）
    def addGossip(self,content,id):
        url='http://gossip.renren.com/gossip.do'
        d={
           'body':content,
           'cc':id,
           'id':id,
           'only_to_me':0,
           'ref':'http://www.renren.com/'+str(id)+'/profile'
           }
        return self.send(url,d)
    #回复留言（主页未测试）
    def addGossipComment(self, comment,data):
        url = 'http://gossip.renren.com/gossip.do'  
        d = {
            'id': data['owner'], 
            'only_to_me': 1,
            'cc': data['from'],
            'mode': 'conversation',
            'body': comment,
            'ref':'http://gossip.renren.com/getgossiplist.do'
        }
        return self.send(url,d)
    #发表文章
    def addText(self,name,title):
        url='http://page.renren.com/'+self.pid+'/note'
        f=open(name,'r')
        d={
           'body':f.read(),
           'pid':self.pid,
           'title':title,
           'isVip':'false',
           'jf_vip_em':'false'
         }
        f.close()
        return self.send(url,d)
    #评论文章
    def addTextComment(self,data):
        url='http://blog.renren.com/PostComment.do'
        if data.has_key('anchor'):cid=data['anchor']
        else :cid=data['comment_id']
        ans=self.getCommentById(data['owner'],data['source'],cid,0)['replyContent']
        ans=self.reply(ans)
        d={
           'comment':'reply %s:%s'%(data['from_name'].encode('utf-8'),ans),
           'feedComment':'true',
           'guestName':'xxx',
           'id':data['source'],
           'itemName':data['blog_title'].encode('utf-8'),
           'owner':data['owner'],
           'repetNo':data['from'],
           'replyToCommentId':cid
        }
        return self.send(url, d)
    #转发
    def resend(self,data):
        url='http://status.renren.com/doing/update.do?fwdRef=status'
        d={
           'c':'塔塔转发:',
           'fwdId':data[u'source'],
           'fwdOwner':data[u'owner'],
           'level':'',
           'raw':'塔塔转发:',
           'statID':''
           }
        return self.send(url,d)
    #获得评论数
    def getrecentcomment(self):
        t=self.getDoings(self.pid,0)
        num=0
        for i in t:
            num+=i[u'comment_count']
        return num
    #整体调度
    def Respond(self,x):
      #  if 1:
      try:
     #   print x
      #  print self.removeNotification(x['notify_id']).text
       # return
        f=0
        if x['type']=='16':
           # print (x['reply_content'])
            ans=self.reply(x['reply_content'],x)
            #print ans
            f=self.addStatuesComment(ans,x)
           # print f
        elif x['type']=='169':f=1
        elif x['type']=='14':  
            ans=self.reply(x['msg_context'],x)
            f=self.addGossipComment(ans,x)         
        elif x['type']=='196':
            if x['replied_id']!=x['from']:me=self.getCommentById(x['owner'], x['source'], x['replied_id'],3)['replyContent']
            else: me=x['doing_content']
            ans=self.reply(me,x)
            f=self.addStatuesComment(ans,x)           
        elif x['type']=='167':
            ans=self.reply(x['doing_content'],x)
            f=self.addShareComment(ans,x)          
        elif x['type']=='58':
            x['replied_id']=x['from']
            ans=self.reply(x['msg_context'],x)
            f=self.addShareComment(ans,x)
        elif x['type']=='172' or x['type']=='17':
            f=self.addTextComment(x)
        if f:self.removeNotification(x['notify_id'],x['type'])
        else:raise
      except Exception,e:
        with open('respond.txt','a') as f:
       #   print x
          f.write(str(x)+'\n')
          self.removeNotification(x['notify_id'],x['type'])
        self.logger.error(e)
    
    def reply(self,mes,x=''):
       # print mes
        mes=re.sub(u'<.*?>','',mes)
        if self.hj==0:
            self.hj=xhj.Xhj()
        ans=''
        if u'转发' in mes or u'扩散' in mes:
            if x['type']!='14':
                self.resend(x)
                ans+='已转发'
                return ans
        if u'捡' in mes or u'拾' in mes:
            print 'jian1'
        if u'丢' in mes or u'掉' in mes:
            print 'shi2'
        l=jieba.cut(mes)#,cut_all=True)
        #print l
        for i in l:
            t=self.sq.find(i)
            if t!=0:
                return t
        #print mes
        return self.hj.chat(mes)
            
        
    

     
if __name__=='__main__':
    s=Renren("czjxy8898@gmail.com","asdf1234",'601654416')
    #s=Renren('rz002@foxmail.com', "lsy2010407637", '256952552')
    #s=Renren("2624908203@qq.com","asdf1234",'601700718')

    s.check()
   # d={'post':'{"id":15651751722,"owner":258288397}'}
    #print s.send('http://share.renren.com/share/ajax.do',d)
    
   # print s.reply('今天天气怎么样'.decode('utf-8'))
    
    #print s.addShare('http://blog.renren.com/share/258288397/15651751722','good')
    #print s.getCommentById('283902768', '4714933905', '468021034',3)['replyContent']
    #for i in range(0,1000):
    #  y=s.session.get('http://notify.renren.com/rmessage/get?getbybigtype=1&bigtype=1&limit=100&begin=0&view=%d'%i).text
    #  if y!='[]':
    #      print i,y
  #  print 'over'
    
    while 1:
     tt=[]
     print 'h'
     try:   
        tt=s.getNotifications()
        time.sleep(1)
        i=0
        print len (tt)
        while i!=len(tt):
           try:
             print tt[i]
             s.Respond(tt[i])
           except Exception,e:
             print Exception,e 
           i+=1
     except Exception,e:
         print Exception,e
         pass
         
    
       


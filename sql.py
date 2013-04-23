# coding:utf-8
import sqlite3
import random
import message


class Sql:

    def __init__(self):
        self.con = sqlite3.connect('tower.db')
        self.con.text_factory = str
        self.cur = self.con.cursor()

    def __del__(self):
        if self.con != 0:
            self.con.commit()
            self.cur.close()
            self.con.close()
            self.con = 0

    def build(self, table, filename):
        if self.con == 0:
            self.__init__()
        try:
            self.cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='%s'" % table)
            s = self.cur.fetchone()
            if s == None:
                self.cur.execute("create table %s (name varchar(1000) primary key)" % table)
            with open(filename, 'r') as f:
                s = f.readline()
                while s != '':
                    self.cur.execute("insert or ignore into %s (name) values('%s')" % (
                        table, s.decode('cp936').encode('utf-8')))
                    s = f.readline()
        except:
            self.__del__()

    def get(self, table):
        if self.con == 0:
            self.__init__()
        try:
            self.cur.execute('select * from %s order by RANDOM() limit 1 ' % table)
            s = self.cur.fetchone()
            s = s[0][:-1] if s[0][-1] == '\n' else s[0]
            s = s.decode('utf-8')
            return s.encode('utf-8')
        except:
            self.__del__()

    def sad(self):
        return self.get('sad')

    def well(self):
        return self.get('well')

    def no(self):
        return self.get('no')

    def poem(self):
        return self.get('poem')

    def update(self):
        if self.con == 0:
            self.__init__()
        m = message.message()
        dic = ['国内新闻', '科技趣闻', '环球视野', '军事汇总', '娱乐八卦', '音乐资讯', '科技要闻', '天气', '农历日历', 'NBA篮球', '教务处', 'Cnbeta', '知乎精选']
        #try:
        for i in range(1, 14):
            print "%s update..." % dic[i-1]
            try:
                s = m.getmsg(i)
            except Exception, e:
                print "%s : get new message error. %s" % (dic[i-1], e)
                continue
            self.cur.execute("select name from message where name = '%s'" % dic[i-1])
            if self.cur.fetchone() == None:
                self.cur.execute("insert into message (ans,name) values('%s','%s')"%(s,dic[i-1]))
            else:
                self.cur.execute("update message set ans='%s' where name=='%s'" % (s, dic[i-1]))
        self.con.commit()
        return 1
        #except  Exception,e:
        #    print e
        #    self.__del__()
        #    return 0

    def find(self, name):
        if self.con == 0:
            self.__init__()
        self.cur.execute("select * from message where name Like '%%%s%%'" % (name))
        t = self.cur.fetchone()
        return t[1] if t != None else 0

if __name__ == "__main__":
    a = Sql()
    del a
    a = Sql()
    print a.update()

   # print a.find('天气')
    # del a
    # a.build('well','3.txt');

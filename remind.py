#coding:utf-8
from datetime import *
def remind():
    now=datetime.now()
    dur=datetime(1970,1,1)-now
    with open('remind.txt','r') as f:
        m=f.readlines()
        i=0
        while i<len(m):
            s=m[i].split()[0]#获取时间串
            zhu=m[i].split()[1]
            that=datetime.strptime('%s'%s,"%Y-%m-%d")
            dur=that-now
            if dur.days<0:i+=1
            else:break
    if i!=0:
        f=open('remind.txt','w')
        f.writelines(m[i:])
        f.close()
    if dur.days>=0:
        if dur.days>2:s='%d天%d小时;  '%(dur.days,dur.seconds/3600)
        else: s='%d小时;  '%(int(dur.total_seconds()/3600))
        return '距%s还有'%zhu+s
    return ""

if __name__=="__main__":
   print  remind().decode('utf-8').encode('cp936')

# -*- coding: UTF-8 -*-
import pymssql
from send_mail import *
import time
def get_sql():
    conn=pymssql.connect(host='119.29.98.161',database='emailremind',user='sa',password='Cxz13299')
    cur=conn.cursor()
    #now_time = judge_time()
    now_time = time.strftime('%Y/%m/%d %H:%M:00',time.localtime(time.time()))
    #print now_time
    #降序排序（升序ASC）
    cur.execute('select * FROM remind  WHERE time=%s and condition=%s' ,(now_time,"no"))
    row = cur.fetchone()
    if row != None:
        get_time = row[3].rstrip()[:-3]
        #如果提醒时间相等，开始提醒并发送邮件
        print '提醒时间 ：'.decode('utf8')+ now_time
        title = '【'.decode('utf8')+row[0].rstrip()+'】'.decode('utf8') +row[1].rstrip()
        print '提醒标题 ：'.decode('utf8')+ title
        content = row[2].rstrip()
        print '提醒内容 ：'.decode('utf8') + content
        list = row[4]
        print '提醒邮箱 ：'.decode('utf8') + list
        send_mail(list,title,content)
        cur.execute('EXEC alter_remind @title=%s,@time=%s,@email=%s',(row[1],row[3],row[4]))
        conn.commit() #提交修改
        print "-----------------------------------"

        #为了防止数据库中还剩余没有提醒过的活动，状态设为yes
        # if now_time > get_time:
        #     cur.execute('EXEC alter_remind @title=%s,@time=%s,@email=%s',(row[1],row[3],row[4]))
        #     conn.commit() #提交修改
        conn.close()

if __name__ == '__main__':
    while 1:
        get_sql()
        time.sleep(10)
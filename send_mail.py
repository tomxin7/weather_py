#-*- coding: utf-8 -*-
import pymssql
import smtplib
import email.MIMEMultipart# import MIMEMultipart
import email.MIMEText# import MIMEText
import email.MIMEBase# import MIMEBase
import random

#通过MSSQL服务器，提取账号密码，并轮流发送邮件模块
def send_mail_demo(to_list,title,content,i):
    #填些服务器IP和账号密码
    conn=pymssql.connect(host='ip地址',database='python',user='数据库账号',password='数据库密码')
    cur=conn.cursor()
    #查询在数据库中有多少个邮箱
    cur.execute('SELECT COUNT(mail_num) FROM mail')
    row = cur.fetchone()
    # print row[0]
    all_num = row[0]
    mail_num = random.randint(1, all_num)
    cur.execute('SELECT * FROM mail WHERE mail_num=%d',( mail_num))
    row = cur.fetchone()
    # for row1 in row:
    #     print row1
    conn.close()
    sub=title
    mail_host=row[1].rstrip()
    mail_user=row[2].rstrip()
    mail_pass=row[3].rstrip()
    mail_postfix=row[4].rstrip()
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg =email.MIMEText.MIMEText(content,_charset="utf-8")
    # msg=MIMEText(content)
    msg['Subject'] =sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    i=0
    try:
        if row[4].rstrip()=="qq.com":
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        else:
            s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        print "邮件发送成功"
        return "ok"
    except Exception, e:
        print str(e)
        if i > 3:
            print "该邮件发送失败"
            return "ok"
        else:
            print "在尝试重新发送"
            return "no"

def send_mail(list,title,content):
    # to_list=["865498311@qq.com"]
    # title="123"
    # content="123"
    flag = "no"
    i=0
    while(flag=="no"):
        flag = send_mail_demo(list,title,content,i)
        i+=1
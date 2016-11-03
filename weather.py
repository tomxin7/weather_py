# -*- coding: UTF-8 -*-
import urllib
import re
import time
import smtplib
from bs4 import BeautifulSoup
import email.MIMEMultipart# import MIMEMultipart
import email.MIMEText# import MIMEText
import email.MIMEBase# import MIMEBase


#获取网页的源码
def get_html(url):
    html = urllib.urlopen(url)
    content = html.read()
    html.close()
    return content

#使用BeautifulSoup模块，提取出所需要的信息
def get_url(info):
    soup = BeautifulSoup(info)
    all_time = soup.find_all('div',class_="time")
    time= all_time[2].string
    all_desc = soup.find_all('div',class_="desc")
    #提取气候
    a=str(all_desc)
    regex = r'.+?class.+?>(.*?)<'
    pat=re.compile(regex,re.S)
    title_code=re.findall(pat,a)
    print title_code[2]
    # desc= all_desc[2].string
    all_temp = soup.find_all('div',class_="temp")
    temp = all_temp[2].string
    return time,title_code[2],temp

#判断是否下雨
def rain(weather):
    #通过正则，模糊匹配到是否有雨
    # message = weather.encode('utf8')
    # (re.search(u'雨'.encode('utf8'), message).group()
    #当字符中含有雨字的话weat返回雨字的位置，没有雨字的话返回-1
    info = weather
    weat= info.find("雨")
    if weat!= -1 :
        return "雨"
    else:
        return "晴"

#发送邮件模块
def send_mail(to_list,sub,content):
    mail_host="smtp.139.com"
    mail_user="13450452462"
    mail_pass="cxz13299"
    mail_postfix="139.com"
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg =email.MIMEText.MIMEText(content,_charset="utf-8")
    # msg=MIMEText(content)
    msg['Subject'] =sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        # s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

#下雨警报
def rain_warning(weather,mailto_list):
    #mailto_list 是要发送的邮箱列表  sub是邮件标题  connect是内容
    connect= "%s \n" % time.ctime()+"尊敬的用户您好，根据中国气象局的预报\n预计： ".decode('utf8') +  weather[0]+ "  会有： ".decode('utf8')+ weather[1].decode('utf8') \
         + "  气温： ".decode('utf8')+ weather[2] +"\n请您外出时注意带伞".decode('utf8')
    if send_mail(mailto_list,"天气下雨温馨提醒",connect):
        print "<下雨提醒>发送成功"
    else:
        print "发送失败"

#取消下雨警报
def rerain_warning(weather,mailto_list):
     #mailto_list 是要发送的邮箱列表  sub是邮件标题  connect是内容
    connect= "%s \n" % time.ctime()+"尊敬的用户您好，根据中国气象局的预报\n预计： ".decode('utf8') +  weather[0]+ "  天气： ".decode('utf8')+ weather[1].decode('utf8') \
     + "  气温： ".decode('utf8')+ weather[2] +"\n取消下雨提示，请您放心出门".decode('utf8')
    if send_mail(mailto_list,"解除下雨提醒",connect):
        print "<解除下雨提醒>发送成功"
    else:
        print "发送失败"


flag="晴"
flag1=1
i=1
while 1:
    if __name__ == '__main__':
        print "获取时间 : %s" % time.ctime()+ "    运行 : %s" % i +"次"
        i+=1
        url="http://m.weathercn.com/eachhours.do?id=101300503&partner="
        # url="http://m.weathercn.com/eachhours.do?id=101050204&partner="
        info =  get_html(url)
        weather = get_url(info)
        connect= "预报时间： ".decode('utf8') +  weather[0]+ "  天气： ".decode('utf8')+ weather[1].decode('utf8') \
                  + "  气温： ".decode('utf8')+ weather[2]
        print connect
        rain_results = rain(weather[1])
        print rain_results
        mailto_list=["865498311@qq.com"]
        # mailto_list=["865498311@qq.com"]
        if rain_results == "雨" and rain_results!=flag and flag1==1:
            rain_warning(weather,mailto_list)
            flag=rain_results
            flag1=2
        if rain_results== "晴" and  rain_results!=flag and flag1==2:
            rerain_warning(weather,mailto_list)
            flag=rain_results
            flag1=1
        #晚上不用提醒
        sleep_now=int(time.strftime('%H',time.localtime(time.time())))
        # print (time.strftime('%H',time.localtime(time.time())))
        if sleep_now <= 6:
            print "系统休眠中,预计6:00再次启动"
            time.sleep(5*60*60)
            flag="晴"
            print "重启成功，继续为您监控天气"
        time.sleep(1800)


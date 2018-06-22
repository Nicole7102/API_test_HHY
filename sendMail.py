#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ConfigParser, os, smtplib
from email.mime.text import MIMEText


# 通过自带的ConfigParser模块，读取邮件发送的配置文件，作为字典返回
def get_conf():
    conf_file = ConfigParser.ConfigParser()
    conf_file.read(os.path.join(os.getcwd(), 'conf.ini'))
    conf = {}
    conf['sender'] = conf_file.get("email", "sender")
    conf['receiver'] = conf_file.get("email", "receiver")
    conf['smtpserver'] = conf_file.get("email", "smtpserver")
    conf['username'] = conf_file.get("email", "username")
    conf['password'] = conf_file.get("email", "password")
    return conf


def sendMail(text):
    mail_info = get_conf()
    sender = mail_info['sender']
    receiver = mail_info['receiver']
    subject = '[AutomationTest]接口自动化测试报告通知'
    smtpserver = mail_info['smtpserver']
    username = mail_info['username']
    password = mail_info['password']
    msg = MIMEText(text, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ''.join(receiver)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    print "邮箱登录成功"
    smtp.sendmail(sender, receiver, msg.as_string())
    print "发送成功"
    smtp.quit()

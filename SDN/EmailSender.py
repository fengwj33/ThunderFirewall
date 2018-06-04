#!/usr/bin/python3
#coding=utf-8
import smtplib
from email.mime.text import MIMEText
def sendEmail(subject,content,msg_to):
    msg_from='1750956766@qq.com' 
    passwd='kawurhdrdozgbdhg'                            
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except s.SMTPException:
        print("发送失败")

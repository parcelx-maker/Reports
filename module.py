#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import RECEIVERS, SENDER, EMAIL_HOST, MAIL_SMTP_PORT, EMAIL_USER, EMAIL_PWD


class Report:
    def __init__(self):
        self.sender = SENDER
        self.receivers = RECEIVERS
        self.email_host = EMAIL_HOST
        self.email_port = MAIL_SMTP_PORT
        self.email_user = EMAIL_USER
        self.email_pwd = EMAIL_PWD
        self.msg = None
        self.title = None
        self.attaches = list()

    def generate(self):
        # generate report
        pass

    def send(self):
        print("开始发生邮件 " + self.title)
        if not self.msg:
            raise ValueError("msg not exist, can not send empty mail!")
        if not self.title:
            raise ValueError("title not exist, can not send mail without title!")
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receivers
        message['Subject'] = Header(self.title, 'utf-8')
        message.attach(MIMEText(self.msg, 'plain', 'utf-8'))
        if self.attaches:
            for attach in self.attaches:
                att = MIMEText(open(attach, 'rb').read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename="' + attach + '"'
                message.attach(att)
        # try:
        so = smtplib.SMTP()
        so.connect(self.email_host, self.email_port)
        so.login(self.email_user, self.email_pwd)
        so.sendmail(self.sender, self.receivers, message.as_string())
        print("邮件发送成功")
        # except smtplib.SMTPException as e:
        #     print("Error: 无法发送邮件" + e.strerror)

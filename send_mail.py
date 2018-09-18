#! /usr/bin/env python
# -*- coding:utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from pathlib import Path
from datetime import datetime
import sys
import os


class MailSender:
    _from = None
    _attachments = []

    def __init__(self, smtpSvr, port):
        self.smtp = smtplib.SMTP()
        print("connecting...")
        self.smtp.connect(smtpSvr, port)
        print("connected!!!")

    def login(self, user, pwd):
        self._from = user
        print("login ...")
        self.smtp.login(user, pwd)

    def add_attachment(self, filename):
        '''
            添加附件
        '''
        attr_name = Path(filename).parts[-1]
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(open(filename, 'rb').read())
        att.add_header('Content-Disposition', 'attachment',
                       filename=('gbk', '', attr_name))
        encoders.encode_base64(att)

        self._attachments.append(att)

    def send(self, subject, content, to_addr):
        '''
            发送邮件
        '''
        msg = MIMEMultipart('alternative')
        contents = MIMEText(content, "html", _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = self._from
        msg['To'] = to_addr
        for att in self._attachments:
            msg.attach(att)
        msg.attach(contents)
        try:
            self.smtp.sendmail(self._from, to_addr.split(','), msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    def close(self):
        self.smtp.quit()
        print("logout.")


def check_latest_file(p, today):
    counter = 0
    for file in p.glob('*.csv'):
        if today in file.name:
            counter += 1
    return counter


def main(date=None):
    user = os.environ.get('EMAIL_NAME')
    pwd = os.environ.get('EMAIL_PWD')
    to_addr = '366138476@qq.com,lucibriel@163.com'
    smtpSvr = 'smtp.exmail.qq.com'
    subject = date + '伊婉销售情况'
    content = '请查看附件'
    if date is None:
        today = datetime.now().strftime('%Y-%m-%d')
    else:
        today = date
    p = Path(r"E:\伊婉销售情况")

    m = MailSender(smtpSvr, 25)
    m.login(user, pwd)
    for file in p.glob('*.csv'):
        if today in file.name:
            m.add_attachment(file)

    m.send(subject, content, to_addr)
    m.close()


if __name__ == '__main__':
    if sys.argv[1]:
        main(sys.argv[1])
    else:
        main()

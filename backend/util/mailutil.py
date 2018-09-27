#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" 邮件发送模块 """

import logging
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import fileutil

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)

mail_host = 'mail.domain.com'
mail_user = 'mailsender'
mail_pass = 'xxxxxxxx'
mail_postfix = 'domain.com'


def send_mail_att(to_list=[], cc_list=[], sub=None, content=None, att_file=None):
    me = '<'+mail_user+'@'+mail_postfix+'>'
    # 创建一个带附件的实例
    msg = MIMEMultipart()

    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    msg['Cc'] = ';'.join(cc_list)
    msg['Accept-Language'] = 'zh-CN'

    # 邮件正文内容
    msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))
    
    if att_file:

        # 构造附件1
        att1 = MIMEText(open(att_file, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        short_name, ext = fileutil.get_file_name_and_ext(att_file)
        file_name = short_name + ext
        att1["Content-Disposition"] = 'attachment; filename=%s' % file_name
        msg.attach(att1)

    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        msg = 'mail has been send to %s, cc %s' % (to_list, cc_list)
        logger.info(msg)
        return True, msg
    except Exception, e:
        msg = 'mail send exception: %s' % str(e)
        logger.error(msg)
        return False, msg


def send_mail_html(to_list=[], cc_list=[], sub=None, content=None):  # to_list：收件人；sub：主题；content：邮件内容
    me = "<"+mail_user+"@"+mail_postfix+">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content, _subtype='html', _charset='utf-8')   # 创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub  # 设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg['Cc'] = ';'.join(cc_list)
    msg['Accept-Language'] = 'zh-CN'
    
    try:
        s = smtplib.SMTP()  
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(me, to_list, msg.as_string())  # 发送邮件
        s.close()
        msg = 'mail has been send to %s, cc %s' % (to_list, cc_list)
        logger.info(msg)
        return True, msg
    except Exception as e:
        msg = 'mail send exception: %s' % str(e)
        logger.error(msg)
        return False, msg


if __name__ == '__main__':
    if sys.argv and len(sys.argv) >= 4:
        print 'args input: %s' % sys.argv
        to_list = str.split(sys.argv[1], ';')
        cc_list = str.split(sys.argv[2], ';')
        if send_mail_att(to_list, cc_list, sys.argv[3], sys.argv[4], sys.argv[5]):
            print 'mail has been send to [%s]' % sys.argv[1]
        else:
            print 'mail send failed'
    else:
        print 'args illegal'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" http server """

__author__ = 'Zachary Bai'

import sys
import os
import logging.config
import yaml
import json
from flask import Flask, request
from werkzeug.utils import secure_filename
from urllib2 import quote
from backend.util import mailutil
from backend.module import respdata

reload(sys)
sys.setdefaultencoding('utf8')

with open('logging.yml') as f:
    D = yaml.load(f)
    D.setdefault('version', 1)
    logging.config.dictConfig(D)

logger = logging.getLogger('main')

UPLOAD_FOLDER = '/data/mail-server/uploads/'  # 邮件附件存储路径
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 上传文件最大16M


def init_dir():
    if not (os.path.exists(UPLOAD_FOLDER) & os.path.isdir(UPLOAD_FOLDER)):
        os.makedirs(UPLOAD_FOLDER, 0755)


@app.route('/')
def hello_world():
    logger.info("get request")
    return 'Mail Flask Server Index!'


@app.route('/mail', methods=['POST'])
def mail():
    resp_data = respdata.RespData()
    logger.debug(request.headers)
    logger.debug(request.form)
    tos = request.form.get('tos', type=str)
    ccs = request.form.get('ccs', default='', type=str)
    subject = request.form.get('subject', default=None, type=str)
    content = request.form.get('content', default=None, type=str)

    has_att = False
    filename = None
    att_file = None
    try:
        att_file = request.files['att_file']
    except Exception, e:
        logger.warning('---- read [att_file] failed! %s', e)

    if att_file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(quote(str(att_file.filename))))
        att_file.save(filename)
        has_att = True

    logger.info('mail to send: content[%s] ,subject[%s], tos[%s], att_file[%s]' % (content, subject, tos, filename))

    if not tos:
        msg = 'tos is None, mail send failed'
        logger.warning(msg)
        resp_data.set_status(False)
        resp_data.set_msg(msg)
        json_data = json.dumps(resp_data.to_dict())
        return json_data

    to_list = str.split(tos, ';')
    logger.debug('to_list: %s' % to_list)
    cc_list = str.split(ccs, ';')
    logger.debug('cc_list: %s' % to_list)
    if has_att:
        success, msg = mailutil.send_mail_att(to_list, cc_list, subject, content, filename)
    else:
        success, msg = mailutil.send_mail_html(to_list, cc_list, subject, content)
    if success:
        logger.info(msg)
    else:
        logger.warning(msg)

    resp_data.set_status(success)
    resp_data.set_msg(msg)
    return json.dumps(resp_data.to_dict())


if __name__ == '__main__':
    init_dir()
    app.run(host='0.0.0.0', port=10086)


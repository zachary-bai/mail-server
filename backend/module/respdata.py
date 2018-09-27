#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" script declare """

__author__ = 'Zachary Bai'


class RespData(dict):
    status = False
    msg = ""
    data = None

    def __init__(self):
        pass

    def get_status(self):
        return self.status

    def set_status(self, status=False):
        self.status = status

    def get_msg(self):
        return self.msg

    def set_msg(self, msg):
        self.msg = msg

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def to_dict(self):
        return self.__dict__


if __name__ == '__main__':
    res = RespData()
    print res
    res.set_msg("test")
    print res.to_dict()

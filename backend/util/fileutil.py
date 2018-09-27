#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 文件处理模块 """

__author__ = 'Zachary Bai'

import os


def get_file_name_and_ext(filename):
    (file_path, temp_file_name) = os.path.split(filename)
    (shot_name, extension) = os.path.splitext(temp_file_name)
    return shot_name, extension


if __name__ == '__main__':
    print get_file_name_and_ext('/home/zachary/test.txt')

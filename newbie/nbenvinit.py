# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'jj'
__mtime__ = '2018/1/15'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import platform
import os

# Platform

nb_platform = 0x00 if 'windows' in platform.platform().lower() else 0x01
nbSlash = '\\' if nb_platform == 0x00 else '/'

# Pre_define

nb_conf_base_dir = nbSlash.join(['', '..', 'conf', ''])
nb_conf_name = "nb_conf.json"
nb_basic_lib_dir = os.path.dirname(__file__)

# python2 or python3
# TODO:the difference between python2 and python3
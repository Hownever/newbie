# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'jj'
__mtime__ = '2017/12/29'
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
import os
import logging
import threading

log_relative_path = '{slash}'.format(slash="/").join(['', '..', 'log', ''])


def singleton(cls):
    """
    Singleton decorator function.
    :param cls: Class object decorated.
    :return the only Instantiation of the class object decorated.
    :attention the class decorated cannot be inheritanced.
    """
    instances = {}
    objs_locker = threading.Lock()

    def _singleton(*args, **kw):
        if args:
            objs_locker.acquire()
            if cls not in instances:
                instances[cls] = {args[0]: cls(*args, **kw)}
            else:
                if args[0] not in instances[cls]:
                    instances[cls][args[0]] = cls(*args, **kw)
            objs_locker.release()
            return instances[cls][args[0]]
        else:
            objs_locker.acquire()
            if cls not in instances:
                instances[cls] = cls(*args, **kw)
            objs_locker.release()
            return instances[cls]
    return _singleton


@singleton
class VmtsLogger(object):
    """
    Vmts logger wrap-class.
    """

    def __init__(self, name, base_dir=os.path.dirname(__file__) + log_relative_path):
        self.formatter = '%(levelname)s - %(asctime)s %(name)s: %(message)s'
        self.formmater_debug = '%(levelname)s - %(asctime)s %(name)s: %(message)s\n\tCall Stack Info:\n\t\tfunction: ' \
                          '%(funcName)s\n\t\tmodule: %(module)s\n\t\tfile: %(pathname)s'

        self.pre_conf = cfg.get_module('vmts_conf')
        self.name = name
        self.fp = base_dir + name + '.log'
        self.debug_mode = self.pre_conf.logger.debug
        self.level = logging.DEBUG if self.debug_mode else logging.INFO
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level)
        self.formatter = self.formatter if not self.debug_mode else self.formmater_debug

        if not os.path.exists(self.fp):
            os.makedirs(base_dir)

        file_handle = logging.handlers.TimedRotatingFileHandler(self.fp, when='D', backupCount=5, encoding='utf-8')
        file_handle.setLevel(self.level)
        console_handle = logging.StreamHandler()
        console_handle.setLevel(self.level)

        self.logger.addHandler(file_handle)
        self.logger.addHandler(console_handle)

    def debug(self, msg):
        """
        wrapper of method 'logger.debug'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.debug(msg)

    def info(self, msg):
        """
        wrapper of method 'logger.info'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.info(msg)

    def warning(self, msg):
        """
        wrapper of method 'logger.warning'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.warning(msg)

    def error(self, msg):
        """
        wrapper of method 'logger.error'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.error(msg)

    def critical(self, msg):
        """
        wrapper of method 'logger.critical'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.critical(msg)

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
from logging import handlers
import threading

log_relative_path = '{slash}'.format(slash="/").join(['', 'log', ''])


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
class NbLogger(object):
    """
    Vmts logger wrap-class.
    """

    def __init__(self, name, base_dir=os.path.dirname(__file__) + log_relative_path):

        if not name:
            raise ValueError("Missing name")

        self.formatter = '%(levelname)s - %(asctime)s %(name)s: %(message)s'
        self.formatter_debug = '%(levelname)s - %(asctime)s %(name)s: %(message)s\n\tCall Stack Info:\n\t\tfunction:' \
                               '%(funcName)s\n\t\tmodule: %(module)s\n\t\tfile: %(pathname)s'
        self.pre_conf = True
        self.name = name
        self.fp = base_dir + name + '.log'
        self.debug_mode = False
        self.level = logging.DEBUG if self.debug_mode else logging.INFO
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.formatter = self.formatter if not self.debug_mode else self.formatter_debug

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        if not self.logger.handlers:
            self.file_handle = logging.handlers.RotatingFileHandler(self.fp, maxBytes=20480000,
                                                                    backupCount=10, encoding='utf-8')
            self.file_handle.setLevel(self.level)
            self.file_handle.setFormatter(logging.Formatter(self.formatter))
            self.console_handle = logging.StreamHandler()
            self.console_handle.setLevel(self.level)
            self.console_handle.setFormatter(logging.Formatter(self.formatter))

            # filter_condition = "18:12:42"
            # file_handle.addFilter(logging.Filter(filter_condition))
            self.logger.addHandler(self.file_handle)
            self.logger.addHandler(self.console_handle)

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

    def remove_handler(self):
        """
        remove handler
        :return:
        """
        self.logger.removeHandler(self.console_handle)

if __name__ == "__main__":
    a = NbLogger("critical1")
    a.critical("jiashuo_a")
    print "-------------------"
    b = NbLogger("critical2")
    b.critical("jiashuo_b")
    print "-------------------"
    c = NbLogger("critical3")
    c.critical("jiashuo_c")
    print "-------------------"
    d = NbLogger("critical4")
    d.critical("jiashuo_d")
    f = NbLogger("")
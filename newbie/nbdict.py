# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'jj'
__mtime__ = '2018/1/16'
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


class DictObject(object):

    def __init__(self, dict_obj):

        self.keys = dict_obj.keys()
        for i in self.keys:
            if isinstance(dict_obj[i], dict):
                self.__setattr__(i,  DictObject(dict_obj[i]))
            else:
                self.__setattr__(i, dict_obj[i])

    def __getitem__(self, item):
        """
        overload __builtin__ method: __getitem__
        :param item: the key of which item`s value you wanna to get.
        :return: value of attribute.
        """

        if not isinstance(self.__getattribute__(item), DictObject):
            return self.__getattribute__(item).__str__()
        else:
            return self.__getattribute__(item)

    def keys(self):
        """
        :return: <list>, set with all keys.
        """

        return self.__dict__.keys()

    def has_key(self, key):
        """
        overload dict`s has_key method.
        :param key: input key.
        :return: <boolean>
        """

        if key in self.__dict__.keys():
            return True
        else:
            return False

    def dumps(self):
        """
        method for dumpping DictObject instance to a Dictionary-Object.
        :return: <dict>
        """

        tmp = dict()
        for i in self.keys:
            value = self.__getattribute__(i)
            if isinstance(value, DictObject):
                tmp[i] = value.dumps()
            else:
                tmp[i] = value
        return tmp

if __name__ == "__main__":
    import nbconf
    a = nbconf.Conf(r"F:\newbie\newbie\conf")
    b = a.conf_dict
    c = DictObject(b)
    print c["logger"]["is_debug"]
    #print c.logger.has_key("is_debug")
    #print c.__dict__
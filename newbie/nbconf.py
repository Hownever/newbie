import os
import json
import threading
from treelib import Tree
from nbenvinit import nbSlash, nb_conf_name


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
class Conf(object):
    """
    loads the specified directory configuration json file,
    and switch it to Tree
    """

    def __init__(self, conf_path):

        if not os.path.isdir(conf_path):
            raise ValueError('conf_path must be an existing directory.')
        self.conf = conf_path + nbSlash + nb_conf_name

        #self.tree = ""
        try:
            with open(self.conf) as fl:
                self.conf_json = fl.read()
                self.conf_dict = json.loads(self.conf_json)
        except ValueError:
                print "[ERROR] No JSON object can be decoded from file - {fl}".format(fl=self.conf)

    def dict_to_tree(self):
        """
        Init tree in the function to reduce memory use,
        dict_obj to tree
        :return: tree obj
        """
        self.tree = Tree()
        self.tree.create_node("ROOT", "root")
        self._dict_to_tree(self.conf_dict, parent="root")
        return self.tree

    def _dict_to_tree(self, dict_obj, parent=None):
        """
        switch dict_obj to tree
        :param dict_obj:dict_obj to tree
        :param parent: father node
        :return: None
        """
        for x in range(len(dict_obj)):
            temp_key = dict_obj.keys()[x]
            temp_value = dict_obj[temp_key]
            if isinstance(temp_value, dict):
                self.tree.create_node("%s" % temp_key, "%s" % temp_key, parent="%s" % parent)
                self._dict_to_tree(temp_value, parent=temp_key)
            else:
                self.tree.create_node("%s" % temp_key, "%s" % temp_key, parent="%s" % parent, data=temp_value)


if __name__ == "__main__":
    a = Conf(r"F:\newbie\newbie\conf")
    print a.dict_to_tree()
    b = Conf(r"F:\newbie\newbie\conf")
    #print b.dict_to_tree().children("logger")
    b.dict_to_tree().update_node("is_debug")
    #print b.dict_to_tree().get_node("is_debug")




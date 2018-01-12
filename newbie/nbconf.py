import os
import json
import threading
from treelib import Tree


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
class CreateTree(object):
    """
    loads the specified directory configuration json file,
    and switch it to Tree
    """

    def __init__(self, conf_path):

        if not os.path.isdir(conf_path):
            raise ValueError('conf_path must be an existing directory.')
        self.conf_path = conf_path
        self.tree = Tree()
        self.tree.create_node("ROOT", "root")

        for root, path, files in os.walk(self.conf_path):
            for filename in files:
                try:
                    with open(root + "/" + filename) as fl:
                        self.conf_json = fl.read()
                        self.conf_dict = json.loads(self.conf_json)
                        self.dict_to_tree(self.conf_dict, parent="root")
                except ValueError:
                        print "[ERROR] No JSON object can be decoded from file - {fl}".format(fl=filename)

    def dict_to_tree(self, dict_obj, parent=None):
        """
        switch dict_obj to tree
        :param dict_obj:dict_obj to tree
        :param parent: father node
        :return: None
        """
        if type(dict_obj) == dict:
            for x in range(len(dict_obj)):
                temp_key = dict_obj.keys()[x]
                temp_value = dict_obj[temp_key]
                self.tree.create_node("%s" % temp_key, "%s" % temp_key, parent="%s" % parent)
                self.dict_to_tree(temp_value, parent=temp_key)
        else:
            self.tree.create_node("%s" % dict_obj, "%s" % dict_obj, parent="%s" % parent)

if __name__ == "__main__":
    a = CreateTree(r"F:\newbie\newbie\conf")
    print a.tree



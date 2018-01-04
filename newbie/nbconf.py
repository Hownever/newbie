# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'jj'
__mtime__ = '2018/1/4'
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
import json


__all__ = ["cfg"]


def singleton(cls):
    """
    Singleton decorator function.
    :param cls: Class object decorated.
    :return: wrap decorated object, and return its self.
    """

    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class Node(object):
    """
    node class of JSON dict-trie.
    """

    def __init__(self, child=None, name=None, value=None, is_leaf=False):
        if child is not None:
            self._check_child(child)

        self._child = list()
        self.child = child
        self.name = name
        self.is_leaf = is_leaf
        if not self.is_leaf and value:
            raise ValueError('Only leaf node own its value.')
        self._value = value

    @staticmethod
    def _check_child(child):
        """
        :param child: child obj, waiting for validating.
        :return: type of input-child-obj
        """
        if type(child) == list:
            if False in set([isinstance(i, Node) for i in child]):
                raise ValueError('child node must be an instance of Node class.')
        elif not isinstance(child, Node):
            raise ValueError('child node must be an instance of Node class.')

        return type(child)

    @property
    def value(self):
        """
        :return: node value. Only leaf-nodes can have a value.
        """
        return self._value

    @value.setter
    def value(self, val):
        """
        :param val: new node value.
        :return: None.
        """
        if self.is_leaf:
            self._value = val
        else:
            raise ValueError('Only leaf node own its value.')

    @property
    def child(self):
        """
        :return: <list> child node instances.
        """
        return self._child

    @child.setter
    def child(self, child_node):
        """
        :param child_node: <Node-class>, childe node, must be instance of Node.
        :return: None.
        """

        if child_node is not None:
            child_type = self._check_child(child_node)
        else:
            raise ValueError('child node must not be None.')

        if child_type == list:
            self._child.extend(child_node)
        elif child_type == object:
            self._child.append(child_node)


@singleton
class DictTrie(object):
    """
    Trie-tree class for loading all the config
    """

    def __init__(self, base_dir=None, **conf_fp):

        self.root = Node(name='vmts-root')
        self.index = dict()
        if base_dir is None:
            base_dir = os.path.dirname(__file__) + '/conf/'
        self.base_dir = base_dir
        if conf_fp:
            sub_root_name = conf_fp.keys()
            for i in sub_root_name:
                with open(self.base_dir + i + '.json') as f:
                    sub_trie = json.loads(f.read())

                sub_root = Node(name=i)
                self.append_child(sub_trie, sub_root)
                self.root.child = sub_root

    def append_child(self, dict_obj, root_node=None):
        """
        :param dict_obj: new dictobj for extend dict-trie tree.
        :param root_node: the root node you wanna to make new dictobj append on,
        :return: None
        """

        root = self.root if root_node is None else root_node

        def create_node(_dict_obj, _root):
            """
            :param _dict_obj: trie child object.
            :param _root: root of trie child object.
            :return: None
            """

            for i in _dict_obj:
                if type(_dict_obj[i]) == dict:
                    n = Node(name=i)
                    _root.child = n
                    create_node(_dict_obj=_dict_obj[i], _root=n)
                elif type(_dict_obj[i]) == list:
                    n = Node(name=i)
                    _root.child = n
                    trans_dict = {}
                    for k in range(len(_dict_obj[i])):
                        trans_dict[k] = _dict_obj[i][k]
                    create_node(_dict_obj=_dict_obj[i], _root=n)
                else:
                    n = Node(name=i, is_leaf=True, value=_dict_obj[i])
                    if n.name in self.index.keys():
                        raise IndexError('Duplicate Index.')
                    self.index[n.name] = n
                    _root.child = n

        create_node(_dict_obj=dict_obj, _root=root)

    def get(self, leaf_name):
        """
        :param leaf_name: <str>, the leaf-node config name.
        :return: <string>, means the value of the config name.
        """

        if leaf_name not in self.index:
            raise IndexError('Isn`t the right leaf name.')

        leaf_node = self.index[leaf_name]

        return leaf_node.value

    def set(self, leaf_name, value):
        """
        :param leaf_name: <str>, the leaf-node config name.
        :param value: new value of the special config.
        :return: None.
        """

        if leaf_name not in self.index:
            raise IndexError('Isn`t the right leaf name.')

        leaf_node = self.index[leaf_name]
        if leaf_node.value != value:
            leaf_node.value = value

    def _traversal_dfs(self, set_root=None):
        """
        :param set_root: Node class, set an optional root node.
        :return: yield a node
        """

        root = self.root if set_root is None else set_root
        if not isinstance(root, Node):
            raise TypeError('root node must be an instance of Node class.')

        if not root.is_leaf:
            for i in root.child:
                yield i
                if not root.is_leaf:
                    self._traversal_dfs(set_root=i)


@singleton
class Predefine(object):
    """
    Predefine variables class
    """

    def __init__(self, base_dir):

        if not os.path.isdir(base_dir):
            raise ValueError('base_dir must be an existing directory.')
        self.base_dir = base_dir
        self._predefine = dict()
        self._module = set()

        for r, d, f in os.walk(self.base_dir):
            for i in f:
                try:
                    root = r
                    with open(root + "/" + i) as fl:
                        dict_obj = json.loads(fl.read())
                        self._module.add((i.split('.')[0], i.split('.')[1], root))
                        #Object(dict_obj=dict_obj)
                except ValueError:
                        print "[ERROR] No JSON object can be decoded from file - {fl}".format(fl=i)

    def list(self):
        """
        list all module-names of predefinition.
        :return: <list>, list of module-names.
        """

        return [i[0] for i in self._module]

    def get_module(self, module_name):
        """
        return dictobject instance of specific module.
        :param module_name: <str>,module name.
        :return: <object>, instance of DictObject.
        """

        return self._predefine[module_name]

    def save(self):
        """
        save predefinitions back to their source-file.
        :return: None
        """

        for i in self._module:
            with open(i[2] + "/" + ''.join(i[0:1]), 'w') as fl:
                fl.write(json.dumps(self._predefine[i[0]].dumps()))

        return None

    def detect(self):
        """
        detect config file variation.
        :return: None
        """




def pre_init():
    """
    Function for predefine pre_init
    :return: singleton instance of class-predefine.
    """

    #base_dir = os.path.dirname(__file__) + pdbd
    #return Predefine(base_dir=base_dir)

if __name__ == "__main__":
    a = Node(child=[1,2,3])
    print a
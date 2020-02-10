# -*- coding: utf-8 -*-
"""UniversalDict

Simple decorator/superclass to convert any class into a dictionary

License:
    MIT License

    Copyright (c) 2020 Thomas Li Fredriksen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""


class UniversalDict(object):
    """Universal dict superclass

    Holds encoder and decoder methods
    """
    SERIALIZABLE_ATTRIBUTES = []
    JSON_OBJECT_IDENTIFIER = None

    DICT_OBJ_CLASS_KEY = '__cls__'

    SERIALIZERS = {}

    def __init__(self, **kwargs):
        """Mock initializer

        Args:
            **kwargs: Accepts any keyword-list
        """
        pass

    def encode(self):
        """Encode object

        Returns:
            dict: Dictionary representation using basic datatypes
        """
        ret = {
            UniversalDict.DICT_OBJ_CLASS_KEY: self.__class__.JSON_OBJECT_IDENTIFIER
        }

        for attr in self.__class__.SERIALIZABLE_ATTRIBUTES:
            ret[attr] = UniversalDict.__encode_cb(getattr(self, attr))

        return ret

    @staticmethod
    def __encode_cb(v):
        """Recursive encoder callback

        Args:
            v:

        Returns:
            dict: Dictionary representation of v
        """
        if isinstance(v, UniversalDict):
            # Recursively encode v
            return v.encode()
        elif isinstance(v, list):
            # Recursively encode each element of the list
            return [
                UniversalDict.__encode_cb(e) for e in v
            ]
        else:
            # v is not a UniversalDict-object, assume everything is dandy
            return v

    @classmethod
    def _decode(cls, input_dict):
        """Decode UniversalDict-based object using known attributes

        Args:
            input_dict:

        Returns:
            input_dict in UniversalDict format
        """

        kwargs = {}

        for attr in cls.SERIALIZABLE_ATTRIBUTES:
            kwargs[attr] = UniversalDict.__decode_cb(input_dict[attr])

        return cls(**kwargs)

    @staticmethod
    def __decode_cb(v):
        """Recursive decoder callback

        Args:
            v: Element to be decoded

        Returns:
            v in UniversalDict format
        """
        if isinstance(v, dict) and UniversalDict.DICT_OBJ_CLASS_KEY in v:
            return UniversalDict.decode(v)
        elif isinstance(v, list):
            return [
                UniversalDict.__decode_cb(e) for e in v
            ]
        else:
            return v

    @staticmethod
    def decode(input_dict):
        """Static decoder

        Args:
            input_dict: Dictionary to be parsed

        Returns:
            input_dict in UniversionDict-format
        """
        dict_obj_class = input_dict.pop(UniversalDict.DICT_OBJ_CLASS_KEY)
        cls = UniversalDict.SERIALIZERS[dict_obj_class]

        return cls._decode(input_dict)


def universal_dict(name, attributes, namespace=None):
    """UniversalDict class decorator

    Will turn any class into UniversalDict

    Args:
        name: name of class
        attributes: attributes to be encoded/decoded
        namespace: Additional namespace

    Returns:
        UniversalDict-compatible class of input-class
    """

    def wrapper(cls):
        """Inner decorator

        Args:
            cls: Input class

        Returns:
            Decorated class
        """

        if namespace:
            qualified_name = '.'.join([namespace, name])
        else:
            qualified_name = name

        class RetCls(UniversalDict):
            SERIALIZABLE_ATTRIBUTES = attributes
            JSON_OBJECT_IDENTIFIER = qualified_name

            def __init__(self, *args, **kwargs):
                super().__init__()

                self.__dict__['_obj'] = cls(*args, **kwargs)

            def __getattr__(self, item):
                """Pass-through to underlying class attributes
                """
                return getattr(self.__dict__['_obj'], item)

            def __setattr__(self, key, value):
                """Pass-through to underlying class attributes
                """
                return setattr(self.__dict__['_obj'], key, value)

            def __str__(self):
                """Pass-through to underlying class attributes
                """
                return str(self.__dict__['_obj'])

            def __repr__(self):
                """Pass-through to underlying class attributes
                """
                return repr(self.__dict__['_obj'])

        assert qualified_name not in UniversalDict.SERIALIZERS
        UniversalDict.SERIALIZERS[qualified_name] = RetCls

        return RetCls

    return wrapper


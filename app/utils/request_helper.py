#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import request, abort
from werkzeug.datastructures import MultiDict, CombinedMultiDict

from app.utils.convert import Convert
from app.utils.time_helper import TimeHelper


class MyRequest:

    """
    简单封装request的的多个方法
    根据结果判断真假 “if xxx”
    其中xxx的值为以下字符的时候：
    任何空的东西（如空字符串，空列表，空字典，None）都等价于False（假）
    任何非空的东西（如字符串，列表，字典）都等价于True（真）
    数字0等价于False
    数字非0等价于True
    """

    @classmethod
    def get_all(cls):
        args = []
        for d in request.args, request.form, request.json:
            if not isinstance(d, MultiDict):
                d = MultiDict(d)
            args.append(d)
        return CombinedMultiDict(args).to_dict()

    @classmethod
    def get(cls, key:str, default=None, type=None):
        """
        获取参数
        :param key:
        :param default:
        :param type:
        :return:
        """
        value = None
        if key in request.form:
            value = request.form.get(key)
        elif key in request.args:
            if type is not None and type == list:
                value = request.args.getlist(key)
            else:
                value = request.args.get(key)
        elif request.get_json(silent=True) and key in request.get_json(silent=True):
            value = request.json.get(key)
        elif default is not None:
            value = default
        else:
            abort(400, "Can't find parameter {0} in request.".format(key))
        if value is not None:
            if type is not None:
                try:
                    return type(value)
                except (TypeError, ValueError) as ex:
                    abort(400, "The argument {0} must be {1}.".format(key, type.__name__))
            else:
                return value
        else:
            return None

    @classmethod
    def get_verify_int(cls, key:str, default=None):
        """
        验证参数是否是整数
        :param key:
        :param default:
        :return:
        """
        return cls.get(key,default=default,type=int)

    @classmethod
    def get_verify_float(cls, key:str, default=None):
        """
        验证参数是否是浮点数
        :param key:
        :param default:
        :return:
        """
        return cls.get(key, default=default, type=float)

    @classmethod
    def get_verify_str(cls, key: str, default=None):
        """
        验证参数是否是字符串
        :param key:
        :param default:
        :return:
        """
        return cls.get(key, default=default, type=str)

    @classmethod
    def get_verify_list(cls, key: str, default=None):
        """
        验证参数是否是list
        :param key:
        :param default:
        :return:
        """
        return cls.get(key, default=default, type=list)

    @classmethod
    def get_verify_dict(cls, key: str, default=None):
        """
        将参数转换为dict
        :param key:
        :param default:
        :return:
        """
        value = cls.get(key, default=default)
        try:
            if value is None or value == "":
                return None
            elif not isinstance(value, dict):
                return json.loads(value)
            else:
                return value
        except:
            abort(400, "The argument {0} must be dict.".format(key))

    @classmethod
    def get_verify_date(cls, key:str, default=None):
        """

        :param key:
        :param default:
        :return:
        """
        value=cls.get(key,default=default)
        try:
            TimeHelper.str_to_datetime(value, "%Y-%m-%d")
            return value
        except:
            abort(400, "The argument {0} must be date like XXXX-XX-XX.".format(key))

    @classmethod
    def get_verify_time(cls, key:str, default=None):
        """
        :param key:
        :param default:
        :return:
        """
        value = cls.get(key,default=default)
        try:
            TimeHelper.str_to_datetime(value, "%H:%M:%S")
            return value
        except Exception as ex:
            abort(400, "The argument {0} must be date like XX:XX:XX.".format(key))

    @classmethod
    def get_verify_datetime(cls, key:str, default=None):
        """
        验证日期字段
        :param key:
        :param default:
        :return:
        """
        value=cls.get(key,default=default)
        try:
            TimeHelper.str_to_datetime(value, "%Y-%m-%d %H:%M:%S")
            return value
        except Exception as ex:
            abort(400, "The argument {0} must be datetime like XXXX-XX-XX XX:XX:XX.".format(key))

    @classmethod
    def get_verify_bool(cls, key:str, default=None):
        """
        验证bool值
        :param key:
        :param default:
        :return:
        """
        value=cls.get(key,default=default)
        try:
            return Convert.to_bool(value)
        except:
            abort(400, "The argument {0} must be {1}.".format(key, type.__name__))

    @classmethod
    def get_verify_empty(cls, key:str):
        """
        验证字符串非空
        :param key:
        :param errmsg:
        :return:
        """
        value=cls.get_verify_str(key)
        if value == "":
            abort(400,"The argument {0} can't be empty.".format(key))
        return value

    @classmethod
    def get_param_default_none(cls, key:str, type=None):
        """
        根据key获取value
        如果不传参数，则默认为None
        :param key:
        :param type:
        :return:
        """
        value = None
        if key in request.form:
            value = request.form.get(key)
        elif key in request.args:
            value = request.args.get(key)
        elif request.get_json(silent=True) and key in request.get_json(silent=True):
            value = request.json.get(key)
        if value is not None:
            if type is not None:
                try:
                    if type == list or type == dict:
                        return json.loads(value)
                    elif type == bool:
                        return Convert.to_bool(value)
                    else:
                        return type(value)
                except Exception as ex:
                    abort(400, "The argument {0} must be {1}.".format(key, type.__name__))
            else:
                return value
        else:
            return None
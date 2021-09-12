#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from app.utils.response_helper import MyResponse

#在蓝本中编写错误处理程序稍有不同，如果使用 errorhandler 修饰器，那么只有蓝本中的错误才
#能触发处理程序。要想注册程序全局的错误处理程序，必须使用 app_errorhandler。

error = Blueprint('error', __name__)

@error.app_errorhandler(400)
def not_found_bad_request(error):
    """
    Bad Request
    如果浏览器发送一些东西给应用，应用或服务器无法处理，则抛出,可用于参数校验
    :param error:
    :return:
    """
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.status = 400
    return myRes.to_json()

@error.app_errorhandler(401)
def not_found_unauthorized(error):
    """
    Unauthorized
    如果用户没有认证则抛出
    :param error:
    :return:
    """
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.status = 401
    return myRes.to_json()

@error.app_errorhandler(403)
def not_found_forbidden(error):
    """
    Forbidden
    如果用户没有权限请求该资源但是已经认证过了，则抛出。
    :param error:
    :return:
    """
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.status = 403
    return myRes.to_json()
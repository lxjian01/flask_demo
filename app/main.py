#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from app.utils.response_helper import MyResponse, ResState

main = Blueprint('main', __name__, url_prefix="/apis")

# check app healthy
@main.route("/check", methods=['GET'])
def check():
    myRes = MyResponse()
    myRes.status = ResState.HTTP_SUCCESS
    myRes.msg = "操作成功"
    return myRes.to_json()
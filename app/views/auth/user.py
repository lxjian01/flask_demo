#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from app import db, log
from app.models.auth import User
from app.utils.response_helper import MyResponse, ResState
from app.utils.sqlalchemy_helper import MySqlalchemy


user = Blueprint('user', __name__, url_prefix="/apis")

@user.route("/users", methods=['POST'])
def add():
    myRes = MyResponse()
    try:
        from app.tasks.tasks import add_task
        result = add_task.delay(23, 42)
        tt = result.wait()
        data = {}
        myRes.data = data
        myRes.status = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except Exception as ex:
        log.error("get user list error by %v", ex)
    return myRes.to_json()

@user.route("/users/page", methods=['GET'])
def page():
    myRes = MyResponse()
    try:
        users = db.session.query(User).all()
        data = MySqlalchemy.to_list(users)
        myRes.data = data
        myRes.status = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except Exception as ex:
        log.error("get user list error by %v", ex)
    return myRes.to_json()

@user.route("/users", methods=['GET'])
def list():
    myRes = MyResponse()
    try:
        users = db.session.query(User).all()
        data = MySqlalchemy.to_list(users)
        myRes.data = data
        myRes.status = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except Exception as ex:
        log.error("get user list error by %v", ex)
    return myRes.to_json()

@user.route("/users/<int:id>", methods=['GET'])
def detail(id):
    myRes = MyResponse()
    try:
        user = db.session.query(User.id, User.user_code).filter(User.id==id).one()
        data = MySqlalchemy.to_dict(user)
        myRes.data = data
        myRes.status = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except Exception as ex:
        log.error("get user detail user id is %d, error by %v", id, ex)
    return myRes.to_json()

@user.route("/users/<int:id>", methods=['DELETE'])
def delete(id):
    myRes = MyResponse()
    try:
        db.session.query(User.id, User.user_code).filter(User.id==id).delete()
        myRes.status = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except Exception as ex:
        log.error("delete user id is %d, error by %v", id, ex)
    return myRes.to_json()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from sqlalchemy import func
from sqlalchemy.engine.row import RowProxy
from sqlalchemy.exc import SQLAlchemyError
from flask import abort

from app import db, log


class MySqlalchemy:
    """
    sqlalchemy帮助类
    """

    @staticmethod
    def add(model):
        """
        添加方法
        :param model:
        :return:
        """
        db.session.add(model)
        db.session.commit()
        return model.to_dict()

    @staticmethod
    def execute(sql):
        db.session.execute(sql)


    @staticmethod
    def add_all(models):
        """
        添加方法
        :param model:
        :return:
        """
        try:
            db.session.add_all(models)
            db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise ex

    @staticmethod
    def delete(model,filters,synchronize_session=None):
        """
        删除方法
        :param model:
        :param filters:
        :return:
        """
        if synchronize_session is not None:
            rows = db.session.query(model).filter(*filters).delete(synchronize_session=synchronize_session)
        else:
            rows = db.session.query(model).filter(*filters).delete()
        db.session.commit()
        return rows

    @staticmethod
    def update(model,filters, attrs,synchronize_session=None):
        """
        修改方法
        :param model:
        :param filters:
        :param attrs:
        :return:
        """
        if synchronize_session is not None:
            rows = db.session.query(model).filter(*filters).update(attrs,synchronize_session=synchronize_session)
        else:
            rows = db.session.query(model).filter(*filters).update(attrs)
        db.session.commit()
        return rows

    @staticmethod
    def __getRealQuery(columns,outerjoins=None, filters=None,orders=None,groups=None):
        """
        私有方法，通用查询方法
        :param columns:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        query=None
        if columns is not None:
            if isinstance(columns, (tuple, list)):
                query = db.session.query(*columns)
            else:
                query = db.session.query(columns)
        if outerjoins is not None:
            if isinstance(outerjoins, (tuple, list)):
                query = query.outerjoin(*outerjoins)
            else:
                query = query.outerjoin(outerjoins)
        if filters is not None:
            if isinstance(filters, (tuple, list)):
                query = query.filter(*filters)
            else:
                query = query.filter(filters)
        if orders is not None:
            if isinstance(orders, (tuple, list)):
                query = query.order_by(*orders)
            else:
                query = query.order_by(orders)
        if groups is not None:
            if isinstance(groups, (tuple, list)):
                query = query.group_by(*groups)
            else:
                query = query.group_by(groups)
        return query

    @staticmethod
    def get_one(columns, outerjoins=None, filters=None,orders=None,groups=None):
        """
        单行查询
        :param columns:
        :param outerjoins:
        :param filters:
        :return:
        """
        query = MySqlalchemy.__getRealQuery(columns, outerjoins=outerjoins, filters=filters, orders=orders,
                                            groups=groups)
        query_data = query.one()
        return MySqlalchemy.to_dict(query_data)

    @staticmethod
    def get_first(columns, outerjoins=None, filters=None,orders=None,groups=None):
        query = MySqlalchemy.__getRealQuery(columns, outerjoins=outerjoins, filters=filters, orders=orders,groups=groups)
        query_data = query.first()
        if query_data:
            return MySqlalchemy.to_dict(query_data)
        else:
            return None

    @staticmethod
    def get_all(columns, outerjoins=None, filters=None, orders=None,groups=None):
        """
        查询所有
        :param columns:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        query = MySqlalchemy.__getRealQuery(columns, outerjoins=outerjoins, filters=filters, orders=orders,
                                            groups=groups)
        query_data = query.distinct().all()
        return MySqlalchemy.to_list(query_data)

    @staticmethod
    def get_count(pk, filters=None):
        """
        查询所有
        :param columns:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        query_total = MySqlalchemy.__getRealQuery(func.count(pk), filters=filters).scalar()
        return query_total

    @staticmethod
    def get_all_limit(columns, outerjoins=None, filters=None, orders=None,groups=None,limit=None):
        """
        查询所有
        :param columns:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        query = MySqlalchemy.__getRealQuery(columns, outerjoins=outerjoins, filters=filters, orders=orders,
                                            groups=groups)
        query_data = query.distinct().limit(limit).all()
        return MySqlalchemy.to_list(query_data)

    @staticmethod
    def get_page_list(pk, columns,current_page, page_size, outerjoins=None, filters=None, orders=None,groups=None):
        """
        分页查询
        :param pk:
        :param columns:
        :param current_page:
        :param page_size:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        if page_size > 100:
            abort(400,"一次最多查询100条数据")
        query = MySqlalchemy.__getRealQuery(columns, outerjoins=outerjoins, filters=filters, orders=orders,
                                            groups=groups)
        query_total = MySqlalchemy.__getRealQuery(func.count(pk), outerjoins=outerjoins, filters=filters, orders=orders,
                                                  groups=groups)
        ###查询
        start_index = (current_page - 1) * page_size
        total = query_total.scalar()
        query_data = query.distinct().limit(page_size).offset(start_index).all()
        return MySqlalchemy.__to_page_dict(query_data, current_page, page_size, total)

    @staticmethod
    def to_list(query_datas):
        """
        将sqlalchemy的query对象转换为list对象
        :param query_datas:
        :return:list
        """
        fields = [MySqlalchemy.to_dict(obj) for obj in query_datas]
        return fields

    @staticmethod
    def to_dict(query_data):
        """
        将sqlalchemy的query对象转换为dict对象
        :param query_data:
        :return:dict
        """
        temp_dict = {}
        if query_data:
            if isinstance(query_data, RowProxy):
                temp_dict = dict(query_data)
            elif hasattr(query_data, '_asdict'):
                temp_dict = query_data._asdict()
            elif hasattr(query_data, 'to_dict'):
                temp_dict = query_data.to_dict()
            else:
                log.error("convert query data to dict error by data {0}".format(str(query_data)))
        return temp_dict


    @staticmethod
    def __to_page_dict(query_datas, current_page, page_size, totals):
        """
        将sqlalchemy的query对象转换为page dict对象
        :param query_datas:
        :return:dict
        """
        data = {}
        data["records"] = MySqlalchemy.to_list(query_datas)
        data["current_page"] = current_page
        data["page_size"] = page_size
        if totals == 0:
            data["pages"] = 1
        else:
            data["pages"] = math.ceil(totals / page_size)
        data["rows"] = totals
        return data
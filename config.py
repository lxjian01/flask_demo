#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = False
    TESTING = False

    THREAD_POOL_EXECUTOR_MAX_WORKER = 60  # max thread pool number

    # 日志文件
    LOG_DIR = "/var/logs"
    LOG_FILE_WEB = "flask-demo.web.log"
    LOG_FILE_CELERY = "flask-demo.celery.log"
    LOG_FILE_CELERY_BEAT = "flask-demo.celery.beat.log"

    # SQLALCHEMY
    SQLALCHEMY_POOL_SIZE = 20  # 数据库连接池的大小
    SQLALCHEMY_POOL_TIMEOUT = 30  # 指定数据库连接池的超时时间
    SQLALCHEMY_MAX_OVERFLOW = 2  # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
    SQLALCHEMY_POOL_RECYCLE = 7200  # 自动回收连接的秒数,8*60*60,超过8小时没用操作就自动断开连接
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # celery配置
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 * 7
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERYD_MAX_TASKS_PER_CHILD = 200  # 每个worker在执行多少次任务后主动销毁重启一个
    CELERYD_CONCURRENCY = 10  # 设置并发worker数量

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    # mysql config
    MYSQL_CONFIG = {"host": "127.0.0.1", "port": 3904,
                    "db": "portal", "user": "root", "passwd": "123456"}
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}'.format(**MYSQL_CONFIG)

    # Celery配置
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False




config = {
    'prod': ProductionConfig,
    'test': TestingConfig,
    'dev': DevelopmentConfig,
    'default': DevelopmentConfig
}

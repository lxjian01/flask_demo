#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor


from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging.config
from app.utils.log import LogHandler
from celery import Celery
# 创建db
db = SQLAlchemy()


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


db.Model.to_dict = to_dict

log = None
logCelery = None
threadPoolExecutor = None


def create_app(config):
    """
    初始化flask web
    :param config:
    :return:
    """

    global log, logCelery, threadPoolExecutor

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    CORS(app)
    db.init_app(app)

    # init log
    logHandler = LogHandler(app)
    logging.config.dictConfig(logHandler.cfg)
    log = logging.getLogger("web")

    # 可以通过连接setup_logging信号来阻止celery配置任何记录器
    from celery.signals import setup_logging
    @setup_logging.connect
    def setup_logging(*args, **kwargs):
        logging.config.dictConfig(logHandler.cfg)

    logCelery = logging.getLogger("celery")

    # init thread poll executor
    thread_max_workers = app.config["THREAD_POOL_EXECUTOR_MAX_WORKER"]
    threadPoolExecutor = ThreadPoolExecutor(thread_max_workers)

    @app.teardown_request
    def teardown_request(exception=None):
        try:
            db.session.remove()
        except Exception as ex:
            print(ex)

    return app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

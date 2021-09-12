#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler

env = os.getenv('FLASK_DEMO_ENV')
if env == "dev":
    LOG_LEVEL = "DEBUG"
else:
    LOG_LEVEL = "INFO"

class LogHandler:
    # log配置字典
    LOG_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s: %(levelname)s/%(processName)s/%(name)s/%(filename)s-%(lineno)d] %(message)s\r",
                # logging会自动在每行log后面添加"\000"换行，windows下未自动换行
            },
            'simple': {
                'format': '%(asctime)s [%(levelname)s] (%(filename)s line:%(lineno)d): %(message)s\r',
            },
        },
        'filters': {},
        'handlers': {
            'console': {
                'level': LOG_LEVEL,
                'class': 'logging.StreamHandler',  # 打印到屏幕
                'formatter': 'simple'
            },
            'web': {
                'level': LOG_LEVEL,
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',  # 支持多进程写日志
                'filename': '/tmp/cmdb-web.log',  # 日志文件
                'maxBytes': 1024 * 1024 * 20,  # 日志大小 20M
                'backupCount': 6,
                'delay': True,  # If delay is true, file opening is deferred until the first call to emit
                'formatter': 'verbose',
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            },
            'celery': {
                'level': LOG_LEVEL,
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',  # 支持多进程写日志
                'filename': '/tmp/cmdb-web.celery.log',  # 日志文件
                'maxBytes': 1024 * 1024 * 20,  # 日志大小 20M
                'backupCount': 6,
                'delay': True,  # If delay is true, file opening is deferred until the first call to emit
                'formatter': 'verbose',
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            },
            'celery_beat': {
                'level': LOG_LEVEL,
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',  # 支持多进程写日志
                'filename': '/tmp/cmdb-web.celery.beat.log',  # 日志文件
                'maxBytes': 1024 * 1024 * 20,  # 日志大小 20M
                'backupCount': 6,
                'delay': True,  # If delay is true, file opening is deferred until the first call to emit
                'formatter': 'verbose',
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            }
        },
        'loggers': {
            'default': {
                'handlers': ['console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': LOG_LEVEL,
                'propagate': False,  # 向上（更高level的logger）传递
            },
            'web': {
                'handlers': ['web'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'celery': {
                'handlers': ['celery'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'celery.beat': {
                'handlers': ['celery_beat'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'celery.task': {
                'handlers': ['celery'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'celery.worker': {
                'handlers': ['celery'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
        },
    }

    def __init__(self, app):
        self.cfg = self.LOG_CONFIG
        log_dir = app.config["LOG_DIR"]
        # 如果不存在定义的日志目录就创建一个
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir, 755)

        # init web log
        log_file_web = app.config["LOG_FILE_WEB"]
        self.cfg['handlers']["web"]['filename'] = os.path.join(log_dir, log_file_web)

        # init celery log
        log_file_celery = app.config["LOG_FILE_CELERY"]
        self.cfg['handlers']["celery"]['filename'] = os.path.join(log_dir, log_file_celery)

        # init celery beat log
        log_file_celery_beat = app.config["LOG_FILE_CELERY_BEAT"]
        self.cfg['handlers']["celery_beat"]['filename'] = os.path.join(log_dir, log_file_celery_beat)





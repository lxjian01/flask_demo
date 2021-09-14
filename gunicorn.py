#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import multiprocessing                                                                                                                                                                 

bind = '0.0.0.0:80'   #绑定的ip及端口号
backlog = 512                #监听队列
workers = 4  # 进程数
worker_class = "gevent"
timeout = 30      #超时
proc_name = 'flask_demo.gunicorn.proc'
max_requests = 20480    #设置一个进程处理完max_requests次请求后自动重启,就是设置这个可以预防内存泄漏，如果不设置的话，则进程不会自动重启
loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置


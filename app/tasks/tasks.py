from __future__ import absolute_import, unicode_literals

from run import celery


@celery.task
def add_task(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y


@celery.task
def xsum(numbers):
    return sum(numbers)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
import datetime
import time
import pytz
from dateutil.relativedelta import relativedelta


class TimeHelper():

    # 1.
    DATATIME_FORMAT="%Y-%m-%d %H:%M:%S"
    DATE_FROMAT="%Y-%m-%d"

    @classmethod
    def localtime(cls):
        return datetime.datetime.now()

    @classmethod
    def datetime_to_str(cls,dt=None,format=None):
        """
        把datetime转成字符串
        :param dt:
        :param format:
        :return:
        """
        if not dt:
            dt=cls.localtime()
        if not format:
            format=cls.DATATIME_FORMAT
        return dt.strftime(format)


    @classmethod
    def str_to_datetime(cls,st,format=None):
        """
        把字符串转成datetime
        :param st:1900-01-01 00:00:00
        :return:
        """
        if not format:
            format = cls.DATATIME_FORMAT
        return datetime.datetime.strptime(st, format)

    @classmethod
    def utc_to_local(cls,utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
        """
        UTCS时间转换为时间戳 2016-07-31T16:00:00Z
        :param utc_time_str:
        :param utc_format:
        :return:
        """
        local_tz = pytz.timezone('Asia/Chongqing')
        local_format = cls.DATATIME_FORMAT
        utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        time_str = local_dt.strftime(local_format)
        return time_str

    @classmethod
    def local_to_utc(cls,local_ts, utc_format='%Y-%m-%dT%H:%MZ'):
        """
        本地时间转换为UTC
        :param local_ts:
        :param utc_format:
        :return:
        """
        local_tz = pytz.timezone('Asia/Chongqing')
        local_format = cls.DATATIME_FORMAT
        time_str = time.strftime(local_format, time.localtime(local_ts))
        dt = datetime.datetime.strptime(time_str, local_format)
        local_dt = local_tz.localize(dt, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        return utc_dt.strftime(utc_format)

    @classmethod
    def get_list_year_month(cls, month_count):
        now = datetime.datetime.now()
        tmp_list = []
        for x in range(month_count):
            datetime_x_month_ago = now - relativedelta(months=x)
            year = datetime_x_month_ago.year
            month = datetime_x_month_ago.month
            if month < 10:
                year_month = "{0}-0{1}".format(year,month)
            else:
                year_month = "{0}-{1}".format(year, month)
            tmp_list.append(year_month)
        return tmp_list

    @classmethod
    def get_month_first_day_and_last_day(cls,month_count):
        now = datetime.datetime.now()
        tmp_list = []
        for x in range(month_count):
            datetime_x_month_ago = now - relativedelta(months=x)
            year = datetime_x_month_ago.year
            month = datetime_x_month_ago.month
            # 获取当月第一天的星期和当月的总天数
            firstDayWeekDay, monthRange = calendar.monthrange(year, month)
            # 获取当月的第一天
            first_day = datetime.datetime(year=year, month=month, day=1, hour=0, minute=0, second=0).strftime(
                "%Y-%m-%d %H:%M:%S")
            last_day = datetime.datetime(year=year, month=month, day=monthRange, hour=23, minute=59,
                                         second=59).strftime("%Y-%m-%d %H:%M:%S")
            tmp_dict = {"year_month": first_day[0:7], "first_day": first_day, "last_day": last_day}
            tmp_list.append(tmp_dict)
        return tmp_list

if __name__ == "__main__":
    # print(TimeHelper.localtime())
    # print(TimeHelper.datetime_to_str(format="%H:%M:%S"))
    # print(TimeHelper.str_to_datetime('09:52:22',"%H:%M:%S"))
    print(TimeHelper.utc_to_local("2016-12-02T00:22:40Z"))
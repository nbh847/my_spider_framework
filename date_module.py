'''
日期处理模块
'''

import datetime
import re
from math import ceil
import monthdelta

# timezone 'Asia/Shanghai'
# from dateutil import relativedelta

tz = datetime.timezone(datetime.timedelta(hours=8))


class Date:
    __tz = tz
    __z = datetime.datetime.now(__tz).strftime('%z')
    __es_z = ':'.join([__z[:3], __z[3:]])
    __time_zone_second = int(__z[:3]) * 3600

    def __init__(self, date=None):
        self.__origin_date = date
        self.__datetime = None

        if date is not None:
            self.__try_datetime(date) or self.__try_date_str(date) or self.__try_timestamp(date)

    @property
    def datetime(self):
        return self.__datetime

    def strftime(self, f, default=None):
        if not self.__datetime:
            return default
        return self.__datetime.strftime(f)

    def timestamp(self, default=0):
        if not self.__datetime:
            return default
        return int(self.__datetime.timestamp())

    def millisecond(self, default=0):
        if not self.__datetime:
            return default
        return self.timestamp() * 1000

    def format(self, default=None, full=True):
        if not self.__datetime:
            return default
        return self.__datetime.strftime('%Y-%m-%d %H:%M:%S' if full else '%Y-%m-%d')

    def format_es_utc_with_tz(self, default=None):
        if not self.__datetime:
            return default
        return self.__datetime.strftime('%Y-%m-%dT%H:%M:%S' + self.__es_z)

    def format_es_old_utc(self, default=None):
        if not self.__datetime:
            return default
        return self.__datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

    def format_es_utc(self, default=None):
        if not self.__datetime:
            return default
        return (self.__datetime - self.__datetime.utcoffset()).strftime('%Y-%m-%dT%H:%M:%SZ')

    def order_year_week(self, default=''):
        if not self.__datetime:
            return default
        year = self.__datetime.strftime('%Y')
        return '%s年第%02d周' % (year, self.year_week_number())

    def year_week(self, default=''):
        if not self.__datetime:
            return default
        year = self.__datetime.strftime('%Y')
        weak = self.__datetime.strftime('%W')
        return '%s年第%s周' % (year, weak)

    def year_week_number(self, default=None):
        if not self.__datetime:
            return default
        day_of_year = int(self.strftime('%j'))
        # week = self.__datetime.strftime('%W')
        # week = int(week)+1
        return ceil((day_of_year + int(Date(self.__datetime).plus_days(-day_of_year).strftime('%w'))) / 7)

    def plus_seconds(self, seconds: float):
        if self.__datetime:
            self.__datetime = self.__datetime + datetime.timedelta(seconds=seconds)
        return self

    def plus_minutes(self, minutes: float):
        if self.__datetime:
            self.__datetime = self.__datetime + datetime.timedelta(minutes=minutes)
        return self

    def plus_hours(self, hours: float):
        if self.__datetime:
            self.__datetime = self.__datetime + datetime.timedelta(hours=hours)
        return self

    def plus_days(self, days: float):
        if self.__datetime:
            self.__datetime = self.__datetime + datetime.timedelta(days)
        return self

    def plus_weeks(self, weeks: float):
        if self.__datetime:
            self.__datetime = self.__datetime + datetime.timedelta(weeks=weeks)
        return self

    def plus_months(self, months: int):
        if self.__datetime:
            self.__datetime = self.__datetime + monthdelta.monthdelta(months)
        return self

    # def plus_years(self, years: int):
    #     if self.__datetime:
    #         self.__datetime = self.__datetime + relativedelta.relativedelta(years=years)
    #     return self

    def to_day_start(self):
        if self.__datetime:
            self.__datetime = self.__datetime.replace(hour=0, minute=0, second=0)
        return self

    def to_day_end(self):
        if self.__datetime:
            self.__datetime = self.__datetime.replace(hour=23, minute=59, second=59)
        return self

    def to_week_start(self):
        if self.__datetime:
            self.__datetime = self.__datetime - datetime.timedelta(self.__datetime.weekday())
            self.to_day_start()
        return self

    def to_week_end(self):
        if self.__datetime:
            self.to_week_start().plus_weeks(1)
            self.__datetime = self.__datetime - datetime.timedelta(seconds=1)
            self.to_day_end()
        return self

    def to_month_start(self):
        if self.__datetime:
            self.__datetime = self.__datetime.replace(day=1, hour=0, minute=0, second=0)
        return self

    def to_month_end(self):
        if self.__datetime:
            self.to_month_start().plus_months(1)
            self.__datetime = self.__datetime - datetime.timedelta(seconds=1)
        return self

    def to_year_start(self):
        if self.__datetime:
            self.__datetime = self.__datetime.replace(month=1, day=1, hour=0, minute=0, second=0)
        return self

    # def to_year_end(self):
    #     if self.__datetime:
    #         self.to_month_start().plus_years(1)
    #         self.__datetime = self.__datetime - datetime.timedelta(seconds=1)
    #     return self

    def clone(self):
        return Date(self.__datetime)

    @staticmethod
    def generator_date(start, end, step_type='day', step=1):
        start = Date(start)
        end = Date(end)
        while start.timestamp() <= end.timestamp():
            yield start.clone()
            if step_type == 'day':
                start.plus_days(step)
            elif step_type == 'month':
                start.plus_months(step)
            elif step_type == 'week':
                start.plus_weeks(step)
            else:
                raise Exception('not support step type: %s', step_type)

    @staticmethod
    def delta_days(date1, date2):
        return Date.delta_seconds(date1, date2) / 86400

    @staticmethod
    def delta_hours(date1, date2):
        return Date.delta_seconds(date1, date2) / 3600

    @staticmethod
    def delta_minutes(date1, date2):
        return Date.delta_seconds(date1, date2) / 60

    @staticmethod
    def delta_seconds(date1, date2):
        return Date(date1).timestamp() - Date(date2).timestamp()

    @classmethod
    def now(cls):
        return cls(datetime.datetime.now(cls.__tz))

    def __try_datetime(self, date):
        if isinstance(date, datetime.datetime):
            self.__datetime = datetime.datetime.fromtimestamp(date.timestamp(), self.__tz)
            return True
        elif isinstance(date, Date):
            self.__datetime = date.datetime
            return True
        else:
            return False

    def __try_timestamp(self, date):
        try:
            self.__datetime = datetime.datetime.fromtimestamp(float(date), self.__tz)
            return True
        except:
            return False

    def __try_date_str(self, date):
        if isinstance(date, str):
            date = date[0:19].replace('T', ' ')
            len_str = len(date)
            arr = re.split("/|-|:| ", date)
            if len(arr) == 1 and len_str != 4:
                return False
            self.__datetime = datetime.datetime.strptime(
                '%s %s' % (' '.join(arr), self.__z),
                ' '.join(['%Y', '%m', '%d', '%H', '%M', '%S'][0:len(arr)]) + ' %z'
            )
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, Date):
            return self.datetime == Date(other).datetime
        return self.datetime == other.datetime

    def __lt__(self, other):
        if not isinstance(other, Date):
            return self.datetime < Date(other).datetime
        return self.datetime < other.datetime

    def __gt__(self, other):
        if not isinstance(other, Date):
            return self.datetime > Date(other).datetime
        return self.datetime > other.datetime

    def __repr__(self):
        return self.format()

# -*- coding: utf-8 -*-

from tunner import useropt

import datetime
import re
import time


def TC_main():
    args = [useropt.vars('time'), useropt.vars('interval')]
    value = next(filter(lambda x: x, args),None)
    if value is None:
        raise ValueError('no --var argument')

    seconds = get_seconds(value)

    print(f'sleeping for {seconds} seconds ...')
    time.sleep(seconds)


def get_seconds(repeat):
    regex_time = re.compile(r'\d+:\d+')
    regex_interval = re.compile(r'(\d+)([hm])')

    matched = None
    seconds = None

    matched = regex_time.match(repeat)
    if matched:
        seconds = get_next(repeat)

    matched = regex_interval.match(repeat)
    if matched:
        interval, unit = matched.groups()
        interval = int(interval)

        if unit == 'm':
            seconds = interval * 60
        elif unit == 'h':
            seconds = interval * 60 * 60
        else:
            pass

    return int(seconds)


def get_next(dailyTime):
    now = datetime.datetime.now()
    today = '%4d-%02d-%02d %s:00' % (now.year,
                                     now.month,
                                     now.day,
                                     dailyTime)
    next = datetime.datetime.strptime(today, '%Y-%m-%d %H:%M:%S')

    if next < now:
        delta = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow = '%4d-%02d-%02d %s:00' % (delta.year,
                                            delta.month,
                                            delta.day,
                                            dailyTime)
        next = datetime.datetime.strptime(tomorrow,
                                          '%Y-%m-%d %H:%M:%S')

    interval = next - now
    seconds = interval.total_seconds()

    return seconds

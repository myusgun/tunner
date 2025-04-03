# -*- coding: utf-8 -*-

from . import useropt

import sys


class Option:
    DEBUG = False


class Internal:
    INITIALIZED = False
    MODULE = ''


def __perror(msg):
    print(msg)
    sys.argv.append('-h')


def __show(clazz):
    opts = {k: v for k, v in clazz.__dict__.items() if k.isupper()}

    print(f'{clazz.__name__}')
    for k, v in opts.items():
        k = '%-15s' % k
        print(f'| {k} = {v}')
    print('-' * 30)


def init():
    if not Internal.INITIALIZED:
        try:
            Option.DEBUG = '--debug' in sys.argv

            if not sys.argv[1].startswith('-'):
                Internal.MODULE = sys.argv[1]

            if debug():
                __show(Option)
                __show(Internal)

            for argv in sys.argv[2:]:
                if argv == '--debug':
                    continue
                elif useropt.on(argv):
                    continue
                else:
                    __perror(f'unknown option: {argv}')
                    break
            else:
                # parse to end
                Internal.INITIALIZED = True

        except IndexError:
            __perror('invalid usage: <module> was not given')

    if debug():
        __show(useropt.Option)

    return Internal.INITIALIZED


def debug():
    return Option.DEBUG


def module():
    if not Internal.MODULE:
        raise ModuleNotFoundError

    return Internal.MODULE

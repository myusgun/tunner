# -*- coding: utf-8 -*-

from . import sysopt
from . import useropt
from .module import Module


def init():
    return sysopt.init()


def help(forced=False):
    return useropt.help(forced)


def run():
    try:
        from importlib import import_module
        module = import_module(sysopt.module())

        return Module(module).run()

    except ModuleNotFoundError as e:
        import sys
        if str(e):
            print(str(e), file=sys.stderr)
        help(forced=True)
        return False

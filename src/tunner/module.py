# -*- coding: utf-8 -*-

from misc.colored import *
from tunner.case import ICase
from tunner import useropt

from datetime import datetime
from datetime import timedelta

import inspect
import traceback


class Module:
    def __init__(self, module):
        # properties
        self.passed = 0
        self.failed = 0
        self.skipped = 0

        self.ok = None
        self.skip = False
        self.forced = False
        self.runtime = timedelta()
        self.lifetime = timedelta()

        # parameter
        self.module = module

    def call(self, target):
        callee = target.callable()
        begin = datetime.now()

        try:
            ret = callee()
            if ret is not None:
                raise Exception(ret)

            self.ok = True

        except Exception as e:
            print(traceback.format_exc(None if useropt.verbose() else 0))
            self.ok = False

        self.runtime = datetime.now() - begin
        self.lifetime += self.runtime

        if self.ok:
            self.passed += 1
        else:
            self.failed += 1

    def result(self):
        if self.skip:
            return Constants.SKIP
        elif self.ok:
            return Constants.PASS
        else:
            return Constants.FAIL

    def init(self):
        try:
            now = str(datetime.now()).split('.')[0]
            print('[   {}   ] {}'.format(Constants.TIME, now))

            targets = (Target.functions(self.module) +
                       Target.classes(self.module))
            targets = sorted(targets, key=lambda x: x.name)

            print(f'[{Constants.DOUBLE_LINE}] Running {len(targets)} tests')

            func = getattr(self.module, 'init', None)
            stat = Constants.AUTO if func else Constants.SKIP
            print(f'[   {stat}   ] Initializing ...')

            if func:
                func()

            return targets

        except:
            print(traceback.format_exc(None if useropt.verbose() else 0))
            return []

    def cleanup(self):
        try:
            do = not useropt.no_cleanup()
            func = getattr(self.module, 'cleanup', None)
            stat = Constants.AUTO if func and do else Constants.SKIP
            print(f'[   {stat}   ] Cleaning up ...')

            if func and do:
                func()

        except:
            print(traceback.format_exc(None if useropt.verbose() else 0))

    def deinit(self):
        try:
            func = getattr(self.module, 'deinit', None)
            stat = Constants.AUTO if func else Constants.SKIP
            print(f'[   {stat}   ] Finalizing ...')

            if func:
                func()

        except:
            print(traceback.format_exc(None if useropt.verbose() else 0))

        print(f'[{Constants.DOUBLE_LINE}]')

        print('[  {} ] {} tests'.format(Constants.SKIPPED, self.skipped))
        print('[  {}  ] {} tests'.format(Constants.PASSED, self.passed))
        print('[  {}  ] {} tests'.format(Constants.FAILED, self.failed))

    def run(self):
        targets = self.init()

        for target in targets:
            if self.__jump_to_next(target):
                continue

            name = '{}.{}'.format(self.module.__name__, target.name)

            print(f'[{Constants.SINGLE_LINE}]')
            print('[ {}      ] {}'.format(Constants.RUN, name))

            if not self.skip:
                self.call(target)

            arg = (self.result(), name, ms(self.runtime))
            print('[     {} ] {} ({})'.format(*arg))

            if not self.ok and useropt.stop_on_fail():
                break

        print(f'[{Constants.SINGLE_LINE}]')
        print('[   {}   ] {}'.format(Constants.TIME, ms(self.lifetime)))

        self.cleanup()
        self.deinit()

        return self.failed == 0

    def __jump_to_next(self, target):
        self.skip = target.is_skipped()
        if self.skip:
            self.skipped += 1
            if useropt.hide_skip():
                return True
        return False


class Target:
    def __init__(self, name, obj):
        def to_name(name):
            return name.upper().replace('_', '-')

        self.name = to_name(name)
        self.unbounded = obj
        self.bounded = None
        self.callee = None

    def callable(self):
        if self.is_function():
            self.callee = self.bounded = self.unbounded
        else:
            self.bounded = self.unbounded()
            self.callee = self.bounded.run

        return self.callee

    def is_skipped(self):
        skip = getattr(self.unbounded, 'skip', False)

        if not skip and useropt.target():
            skip = not is_patterned(self.name, useropt.target())

        if not skip:
            skip = is_patterned(self.name, useropt.skip())

        # although the target seems to be skipped,
        #  target will be run forcely if target was given in options.
        if skip and self.name in useropt.target():
            skip = False

        return skip

    def is_function(self):
        return inspect.isfunction(self.unbounded)

    def is_class(self):
        return inspect.isclass(self.unbounded)

    @staticmethod
    def functions(module):
        tuples = inspect.getmembers(module, inspect.isfunction)
        return [Target(name, obj) for name, obj in tuples if name.startswith('TC')]

    @staticmethod
    def classes(module):
        def is_target_class(obj):
            return inspect.isclass(obj) and issubclass(obj, ICase)

        tuples = inspect.getmembers(module, is_target_class)
        return [Target(name, obj) for name, obj in tuples if name.startswith('TC')]


def ms(delta):
    return '%.2f ms' % (delta.total_seconds() * 1000)


def is_patterned(name, opts):
    import fnmatch
    return any(fnmatch.fnmatch(name, opt) for opt in opts)


class Constants:
    WIDTH = 10
    DOUBLE_LINE = '=' * WIDTH
    SINGLE_LINE = '-' * WIDTH
    AUTO = yellow('AUTO')
    TIME = white('TIME')
    RUN = cyan('RUN')
    PASS = green('PASS')
    FAIL = red('FAIL')
    SKIP = magenta('SKIP')
    PASSED = green('PASSED')
    FAILED = red('FAILED')
    SKIPPED = magenta('SKIPPED')

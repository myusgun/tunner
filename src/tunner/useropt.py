# -*- coding: utf-8 -*-

import sys


class Option:
    HELP = False
    VERBOSE = 0
    HIDE_SKIP = False
    TARGET = ''
    SKIP = ''
    NO_CLEANUP = False
    STOP_ON_FAIL = False
    VARS = {}


GENERAL_OPTIONS = {
    '--help, -h': 'show this',
    '-v, -vv, ...': 'set verbose level',
    '--hide-skip': 'DO NOT show skipped target(s)'
}

CONTROL_OPTIONS = {
    '--target=<TC-nnnn[,TC-mmmm[,...]]>': 'set the target(s) (wildcard is available)',
    '--skip=<TC-nnnn[,TC-mmmm[,...]]>': 'skip target(s) (wildcard is available)',
    '--no-cleanup': 'DO NOT call cleanup() function on end',
    '--stop-on-fail': 'stop on failure',
}

CUSTOM_OPTIONS = {
    '--var=<key:value>': 'set user variable for target',
}


def __get_option_value(argv):
    return argv.split('=').pop()


def on(argv):
    if argv in ['--help', '-h']:
        Option.HELP = True

    elif argv.startswith('-v') and len([c for c in argv[1:] if c != 'v']) == 0:
        Option.VERBOSE = argv.count('v')

    elif argv == '--hide-skip':
        Option.HIDE_SKIP = True

    elif argv.startswith('--target='):
        Option.TARGET = __get_option_value(argv).split(',')

    elif argv.startswith('--skip='):
        Option.SKIP = __get_option_value(argv).split(',')

    elif argv == '--no-cleanup':
        Option.NO_CLEANUP = True

    elif argv == '--stop-on-fail':
        Option.STOP_ON_FAIL = True

    elif argv.startswith('--var='):
        key, value = __get_option_value(argv).split(':')
        Option.VARS[key] = value

    else:
        # unknown option
        Option.HELP = True
        return False

    return True


def help(forced):
    if not (Option.HELP or forced):
        return False

    def printopts(dic):
        for opt, desc in dic.items():
            opt = '%-40s' % opt
            print(f'  {opt}{desc}')

    print(f'usage: {sys.argv[0]} <module> [options]')

    print('\nGeneral optons')
    printopts(GENERAL_OPTIONS)

    print('\nControl optons')
    printopts(CONTROL_OPTIONS)

    print('\nCustom options')
    printopts(CUSTOM_OPTIONS)

    print()

    return True


def verbose(as_level=False):
    return Option.VERBOSE if as_level else Option.VERBOSE > 0


def hide_skip():
    return Option.HIDE_SKIP


def target():
    return Option.TARGET


def skip():
    return Option.SKIP


def no_cleanup():
    return Option.NO_CLEANUP


def stop_on_fail():
    return Option.STOP_ON_FAIL


def vars(key, default=None):
    return Option.VARS.get(key, default)

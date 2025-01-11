# -*- coding: utf-8 -*-

CYAN = ''
GREEN = ''
MAGENTA = ''
RED = ''
WHITE = ''
RESET = ''

try:
    import colorama

    colorama.just_fix_windows_console()
    colorama.init()

    CYAN = colorama.Fore.CYAN
    GREEN = colorama.Fore.GREEN
    MAGENTA = colorama.Fore.MAGENTA
    RED = colorama.Fore.RED
    WHITE = colorama.Fore.WHITE
    YELLOW = colorama.Fore.YELLOW

    RESET = colorama.Style.RESET_ALL

except:
    pass


def colored(color, s):
    return color + s + RESET


def cyan(s):
    return colored(CYAN, s)


def green(s):
    return colored(GREEN, s)


def magenta(s):
    return colored(MAGENTA, s)


def red(s):
    return colored(RED, s)


def white(s):
    return colored(WHITE, s)


def yellow(s):
    return colored(YELLOW, s)

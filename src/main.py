# -*- coding: utf-8 -*-

import tunner


def main():
    if not tunner.init():
        tunner.help(forced=True)
        return 1

    if tunner.help():
        return 0

    ok = tunner.run()
    return 0 if ok else 1


if __name__ == '__main__':
    exit(main())

# -*- coding: utf-8 -*-


def skip(func, *args, **kwargs):
    def decorated():
        return func(*args, **kwargs)
    setattr(decorated, 'skip', True)
    return decorated


class ICase(object):
    def __init__(self):
        self.init()

    def init(self):
        pass

    def run(self):
        raise NotImplementedError

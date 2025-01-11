# -*- coding: utf-8 -*-


def name(length=8, prefix='', suffix='', delim='-'):
    import uuid

    value = uuid.uuid4().hex.lower()[:length]

    ret = ''

    if prefix:
        ret += prefix + delim

    ret += value

    if suffix:
        ret += delim + suffix

    return ret

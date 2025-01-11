# -*- coding: utf-8 -*-

from tunner import case


# --------------------------------------------------------------


def init():
    print("this is init() function")


def cleanup():
    print("this is cleanup() function")


def deinit():
    print("this is deinit() function")


# --------------------------------------------------------------


def TC_0001():
    print("this is a function for test case 0001")


@case.skip
def TC_0002():
    print("this is not called")


class TC_0003(case.ICase):
    def init(self):
        print("this is an init() method")

    def run(self):
        print("this is a run() method")


class TC_0004(case.ICase):
    def run(self):
        print("init() is optional")


class TC_0005(case.ICase):
    def init(self):
        print("but, run() is required")


@case.skip
class TC_0007(case.ICase):
    def init(self):
        print("this is not called")

    def run(self):
        print("this is not called")

# -*- coding: utf-8 -*-

from tunner import useropt

import subprocess


def TC():
    script = useropt.vars('command')
    subprocess.call(['sh', '-c', script])


'''
example
$> python main.py target.shell.command --var=command:"echo ?"
'''

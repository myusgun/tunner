# -*- coding: utf-8 -*-

from tunner import useropt

import subprocess


def TC():
    script = useropt.vars('script')
    subprocess.call(['sh', script])


'''
example
$> python main.py target.shell.script --var=script:script.sh
'''

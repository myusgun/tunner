# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import time


sleep = time.sleep

now = datetime.now
utc = timezone.utc


class timechecker:
    def __init__(self, seconds):
        self.seconds = seconds
        self.end = datetime.now()
        self.reset()

    def reset(self):
        self.end += timedelta(seconds=self.seconds)

    def expired(self):
        return self.end < datetime.now()

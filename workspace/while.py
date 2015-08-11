#!/usr/bin/env python
from x100daemon import Daemon
import time, sys


d = Daemon('/tmp/a.pid')
d.daemonize()

count = 0
while True:
    time.sleep(1)
    print(count)
    count += 1
    if count == 10:
        sys.exit(1)


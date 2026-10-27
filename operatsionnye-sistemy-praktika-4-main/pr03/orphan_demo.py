#!/usr/bin/env python3
import os
import time

pid = os.fork()
if pid == 0:
    time.sleep(2)
    print(f"Orphan child PID={os.getpid()} new PPID={os.getppid()}")
    time.sleep(3)
else:
    print(f"Parent PID={os.getpid()} exits, child PID={pid} becomes orphan")

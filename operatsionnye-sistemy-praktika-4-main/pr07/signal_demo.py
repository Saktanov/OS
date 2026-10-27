#!/usr/bin/env python3
import os
import signal
import time

def handler(signum, frame):
    print(f"caught signal {signum}, process continues")

signal.signal(signal.SIGINT, handler)
print(f"PID={os.getpid()}, press Ctrl+C or run: kill -INT {os.getpid()}")
while True:
    time.sleep(1)

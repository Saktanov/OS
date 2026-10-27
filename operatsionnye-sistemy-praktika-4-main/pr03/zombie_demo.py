#!/usr/bin/env python3
import os
import time

pid = os.fork()
if pid == 0:
    os._exit(0)

print(f"Child {pid} exited, parent sleeps. Run: ps -o pid,ppid,stat,cmd -p {pid}")
time.sleep(20)
os.wait()
print("Zombie was reaped by wait()")

#!/usr/bin/env python3
import os

pid = os.fork()

if pid == 0:
    print(f"Я ребёнок, PID={os.getpid()}, PPID={os.getppid()}")
    os._exit(0)
else:
    finished_pid, status = os.wait()
    code = os.waitstatus_to_exitcode(status)
    print(f"Я родитель, PID={os.getpid()}, дождался PID={finished_pid}, code={code}")

#!/usr/bin/env python3
import os
import sys
import time

if len(sys.argv) < 3:
    print("Usage: python3 runner.py <N> <command> [args...]")
    raise SystemExit(1)

count = int(sys.argv[1])
command = sys.argv[2:]
children = {}

for i in range(count):
    start = time.monotonic()
    pid = os.fork()
    if pid == 0:
        os.execvp(command[0], command)
    children[pid] = start

while children:
    pid, status = os.wait()
    start = children.pop(pid)
    code = os.waitstatus_to_exitcode(status)
    elapsed = time.monotonic() - start
    print(f"pid={pid} code={code} elapsed={elapsed:.3f}s")

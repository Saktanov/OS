#!/usr/bin/env python3
import multiprocessing
import threading

shared = []

def append_value(value: str) -> None:
    shared.append(value)

thread = threading.Thread(target=append_value, args=("thread",))
thread.start()
thread.join()
print("after thread:", shared)

process = multiprocessing.Process(target=append_value, args=("process",))
process.start()
process.join()
print("after process:", shared)

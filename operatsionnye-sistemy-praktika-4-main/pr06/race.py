#!/usr/bin/env python3
import threading

counter = 0

def worker() -> None:
    global counter
    for _ in range(100_000):
        value = counter
        value += 1
        counter = value

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)

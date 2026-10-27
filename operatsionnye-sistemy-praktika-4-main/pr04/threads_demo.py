#!/usr/bin/env python3
import threading
import time

counter = 0

def worker(index: int) -> None:
    global counter
    for _ in range(100_000):
        value = counter
        value += 1
        counter = value
    print(f"thread {index} done")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
start = time.perf_counter()
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
elapsed = time.perf_counter() - start
print(f"counter={counter}, expected=400000, elapsed={elapsed:.4f}s")

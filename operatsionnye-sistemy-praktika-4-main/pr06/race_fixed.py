#!/usr/bin/env python3
import threading
import time

counter = 0
lock = threading.Lock()

def worker() -> None:
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1

start = time.perf_counter()
threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"counter={counter}, elapsed={time.perf_counter() - start:.4f}s")
assert counter == 400_000

#!/usr/bin/env python3
import threading
from collections import deque

CAPACITY = 5
PRODUCERS = 3
CONSUMERS = 2
ITEMS = 1000

buffer = deque()
empty = threading.Semaphore(CAPACITY)
full = threading.Semaphore(0)
mutex = threading.Lock()
consumed = []

def producer(pid: int) -> None:
    for i in range(ITEMS):
        item = (pid, i)
        empty.acquire()
        with mutex:
            buffer.append(item)
            assert len(buffer) <= CAPACITY
        full.release()

def consumer() -> None:
    while True:
        full.acquire()
        with mutex:
            item = buffer.popleft()
        empty.release()
        if item is None:
            break
        consumed.append(item)

consumers = [threading.Thread(target=consumer) for _ in range(CONSUMERS)]
producers = [threading.Thread(target=producer, args=(i,)) for i in range(PRODUCERS)]
for t in consumers + producers:
    t.start()
for t in producers:
    t.join()
for _ in consumers:
    empty.acquire()
    with mutex:
        buffer.append(None)
    full.release()
for t in consumers:
    t.join()
assert len(consumed) == PRODUCERS * ITEMS
assert len(set(consumed)) == PRODUCERS * ITEMS
print("ok", len(consumed))

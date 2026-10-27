#!/usr/bin/env python3
import threading
from collections import deque

CAPACITY = 5
buffer = deque()
condition = threading.Condition()
produced = 100
consumed = []
done = False

def producer() -> None:
    global done
    for item in range(produced):
        with condition:
            while len(buffer) >= CAPACITY:
                condition.wait()
            buffer.append(item)
            condition.notify_all()
    with condition:
        done = True
        condition.notify_all()

def consumer() -> None:
    while True:
        with condition:
            while not buffer and not done:
                condition.wait()
            if not buffer and done:
                return
            item = buffer.popleft()
            condition.notify_all()
        consumed.append(item)

threads = [threading.Thread(target=consumer) for _ in range(2)]
prod = threading.Thread(target=producer)
for t in threads + [prod]:
    t.start()
for t in threads + [prod]:
    t.join()
assert sorted(consumed) == list(range(produced))
print("ok")

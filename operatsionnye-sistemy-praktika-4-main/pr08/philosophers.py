#!/usr/bin/env python3
import threading
import time

N = 5
forks = [threading.Lock() for _ in range(N)]
counts = [0] * N
stop = False

def philosopher(i: int) -> None:
    left = i
    right = (i + 1) % N
    first, second = sorted([left, right])
    while not stop:
        with forks[first]:
            with forks[second]:
                counts[i] += 1
        time.sleep(0.001)

threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
for t in threads:
    t.start()
time.sleep(2)
stop = True
for t in threads:
    t.join()
print(counts)

#!/usr/bin/env python3
import random
import threading

accounts = [1000, 1000, 1000]
initial_total = sum(accounts)
lock = threading.Lock()

def transfer_many() -> None:
    rng = random.Random()
    for _ in range(10_000):
        src, dst = rng.sample(range(len(accounts)), 2)
        amount = rng.randint(1, 5)
        with lock:
            if accounts[src] >= amount:
                accounts[src] -= amount
                accounts[dst] += amount
            assert sum(accounts) == initial_total

threads = [threading.Thread(target=transfer_many) for _ in range(2)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(accounts, sum(accounts))

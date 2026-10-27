#!/usr/bin/env python3
import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def work(name: str) -> None:
    with lock_a:
        time.sleep(0.1)
        with lock_b:
            print(name)

threads = [threading.Thread(target=work, args=(name,)) for name in ("first", "second")]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print("no deadlock")

#!/usr/bin/env python3
import faulthandler
import threading
import time

faulthandler.dump_traceback_later(5, repeat=False)
lock_a = threading.Lock()
lock_b = threading.Lock()

def first() -> None:
    with lock_a:
        time.sleep(0.2)
        with lock_b:
            print("first")

def second() -> None:
    with lock_b:
        time.sleep(0.2)
        with lock_a:
            print("second")

threading.Thread(target=first).start()
threading.Thread(target=second).start()

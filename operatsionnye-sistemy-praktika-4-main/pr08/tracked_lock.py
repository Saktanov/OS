#!/usr/bin/env python3
import threading
import time

wait_for = {}
owners = {}
graph_lock = threading.Lock()

def has_cycle(start, node, seen):
    if node == start:
        return True
    if node in seen:
        return False
    seen.add(node)
    return any(has_cycle(start, nxt, seen) for nxt in wait_for.get(node, set()))

class TrackedLock:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()

    def acquire(self):
        tid = threading.get_ident()
        with graph_lock:
            owner = owners.get(self.name)
            if owner is not None:
                wait_for.setdefault(tid, set()).add(owner)
                if has_cycle(tid, owner, set()):
                    raise RuntimeError("deadlock cycle detected")
        self.lock.acquire()
        with graph_lock:
            owners[self.name] = tid
            wait_for.get(tid, set()).discard(owners.get(self.name))

    def release(self):
        with graph_lock:
            owners.pop(self.name, None)
        self.lock.release()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()

a = TrackedLock("a")
b = TrackedLock("b")

def one():
    with a:
        time.sleep(0.1)
        with b:
            pass

def two():
    with b:
        time.sleep(0.1)
        with a:
            pass

for fn in (one, two):
    threading.Thread(target=fn).start()

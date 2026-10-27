#!/usr/bin/env python3
import os
import resource
import time

data = [0] * 5_000_000

def rss_mb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024

pid = os.fork()
if pid == 0:
    print(f"child before write rss={rss_mb():.1f} MB")
    for i in range(0, len(data), 1000):
        data[i] = 1
    print(f"child after write rss={rss_mb():.1f} MB")
    time.sleep(1)
    os._exit(0)
os.wait()
print(f"parent rss={rss_mb():.1f} MB")

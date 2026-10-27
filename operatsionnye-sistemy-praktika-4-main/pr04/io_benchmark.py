#!/usr/bin/env python3
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URLS = ["https://example.com"] * 20

def fetch(url: str) -> int:
    with urllib.request.urlopen(url, timeout=10) as response:
        return len(response.read())

def run(name: str, func) -> None:
    start = time.perf_counter()
    total = func()
    elapsed = time.perf_counter() - start
    print(f"{name}: bytes={total}, elapsed={elapsed:.3f}s")

run("sequential", lambda: sum(fetch(url) for url in URLS))
run("threads", lambda: sum(ThreadPoolExecutor(max_workers=4).map(fetch, URLS)))

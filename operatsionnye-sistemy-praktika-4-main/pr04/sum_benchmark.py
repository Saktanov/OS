#!/usr/bin/env python3
from __future__ import annotations

import statistics
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path

PATH = Path("numbers.txt")


def load_numbers() -> list[int]:
    if not PATH.exists():
        raise SystemExit("Run python3 gen_numbers.py first")
    return [int(line) for line in PATH.read_text().splitlines()]


def chunk_sum(chunk: list[int]) -> int:
    return sum(chunk)


def split_chunks(values: list[int], n: int) -> list[list[int]]:
    size = (len(values) + n - 1) // n
    return [values[i : i + size] for i in range(0, len(values), size)]


def bench(name: str, func) -> None:
    times = []
    result = None
    for _ in range(3):
        start = time.perf_counter()
        result = func()
        times.append(time.perf_counter() - start)
    print(f"{name:16s} result={result} median={statistics.median(times):.4f}s")


values = load_numbers()
chunks = split_chunks(values, 4)

bench("single", lambda: sum(values))

def threaded() -> int:
    with ThreadPoolExecutor(max_workers=4) as pool:
        return sum(pool.map(chunk_sum, chunks))

def processed() -> int:
    with ProcessPoolExecutor(max_workers=4) as pool:
        return sum(pool.map(chunk_sum, chunks))

bench("4 threads", threaded)
bench("4 processes", processed)

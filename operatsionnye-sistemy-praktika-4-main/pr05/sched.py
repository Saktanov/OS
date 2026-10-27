#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int = 0


def read_processes(path: str) -> list[Process]:
    result = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split()
            pid, arrival, burst = parts[:3]
            priority = int(parts[3]) if len(parts) > 3 else 0
            result.append(Process(pid, int(arrival), int(burst), priority))
    return sorted(result, key=lambda p: (p.arrival, p.pid))


def merge(intervals: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    merged = []
    for start, end, pid in intervals:
        if start == end:
            continue
        if merged and merged[-1][2] == pid and merged[-1][1] == start:
            merged[-1] = (merged[-1][0], end, pid)
        else:
            merged.append((start, end, pid))
    return merged


def fcfs(processes: list[Process]) -> list[tuple[int, int, str]]:
    time = 0
    intervals = []
    for p in processes:
        time = max(time, p.arrival)
        intervals.append((time, time + p.burst, p.pid))
        time += p.burst
    return intervals


def sjf(processes: list[Process]) -> list[tuple[int, int, str]]:
    pending = processes[:]
    time = 0
    intervals = []
    while pending:
        ready = [p for p in pending if p.arrival <= time]
        if not ready:
            time = min(p.arrival for p in pending)
            continue
        p = min(ready, key=lambda item: (item.burst, item.arrival, item.pid))
        pending.remove(p)
        intervals.append((time, time + p.burst, p.pid))
        time += p.burst
    return intervals


def srtf(processes: list[Process]) -> list[tuple[int, int, str]]:
    remaining = {p.pid: p.burst for p in processes}
    by_pid = {p.pid: p for p in processes}
    done = set()
    time = min(p.arrival for p in processes)
    intervals = []
    while len(done) < len(processes):
        ready = [p for p in processes if p.arrival <= time and p.pid not in done]
        if not ready:
            time += 1
            continue
        p = min(ready, key=lambda item: (remaining[item.pid], item.arrival, item.pid))
        intervals.append((time, time + 1, p.pid))
        remaining[p.pid] -= 1
        time += 1
        if remaining[p.pid] == 0:
            done.add(p.pid)
    return merge(intervals)


def priority_preemptive(processes: list[Process]) -> list[tuple[int, int, str]]:
    remaining = {p.pid: p.burst for p in processes}
    done = set()
    time = min(p.arrival for p in processes)
    intervals = []
    while len(done) < len(processes):
        ready = [p for p in processes if p.arrival <= time and p.pid not in done]
        if not ready:
            time += 1
            continue
        p = min(ready, key=lambda item: (item.priority, item.arrival, item.pid))
        intervals.append((time, time + 1, p.pid))
        remaining[p.pid] -= 1
        time += 1
        if remaining[p.pid] == 0:
            done.add(p.pid)
    return merge(intervals)


def rr(processes: list[Process], quantum: int) -> list[tuple[int, int, str]]:
    remaining = {p.pid: p.burst for p in processes}
    by_pid = {p.pid: p for p in processes}
    processes = sorted(processes, key=lambda p: (p.arrival, p.pid))
    queue: deque[str] = deque()
    time = processes[0].arrival
    index = 0
    intervals = []

    def add_arrivals(up_to: int) -> None:
        nonlocal index
        while index < len(processes) and processes[index].arrival <= up_to:
            queue.append(processes[index].pid)
            index += 1

    add_arrivals(time)
    while queue or index < len(processes):
        if not queue:
            time = processes[index].arrival
            add_arrivals(time)
        pid = queue.popleft()
        run = min(quantum, remaining[pid])
        start = time
        end = time + run
        time = end
        remaining[pid] -= run
        intervals.append((start, end, pid))
        add_arrivals(time)
        if remaining[pid] > 0:
            queue.append(pid)
    return intervals


def metrics(processes: list[Process], intervals: list[tuple[int, int, str]]) -> dict[str, float]:
    by_pid = {p.pid: p for p in processes}
    completion = {}
    first_start = {}
    busy = 0
    for start, end, pid in intervals:
        busy += end - start
        completion[pid] = end
        first_start.setdefault(pid, start)
    turnaround = {}
    waiting = {}
    response = {}
    for pid, p in by_pid.items():
        turnaround[pid] = completion[pid] - p.arrival
        waiting[pid] = turnaround[pid] - p.burst
        response[pid] = first_start[pid] - p.arrival
    total_time = max(end for _, end, _ in intervals) - min(p.arrival for p in processes)
    return {
        "avg_wait": sum(waiting.values()) / len(processes),
        "avg_turnaround": sum(turnaround.values()) / len(processes),
        "avg_response": sum(response.values()) / len(processes),
        "cpu_util": busy / total_time if total_time else 1.0,
    }


def print_gantt(intervals: list[tuple[int, int, str]]) -> None:
    print("Gantt:")
    print(" | ".join(f"{s}-{e}:{pid}" for s, e, pid in intervals))


def simulate(processes: list[Process], algorithm: str, quantum: int) -> list[tuple[int, int, str]]:
    if algorithm == "fcfs":
        return fcfs(processes)
    if algorithm == "sjf":
        return sjf(processes)
    if algorithm == "srtf":
        return srtf(processes)
    if algorithm == "priority":
        return priority_preemptive(processes)
    if algorithm == "rr":
        return rr(processes, quantum)
    raise ValueError(algorithm)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--algo", choices=["fcfs", "sjf", "srtf", "priority", "rr"], default="fcfs")
    parser.add_argument("--quantum", type=int, default=3)
    args = parser.parse_args()

    processes = read_processes(args.file)
    intervals = simulate(processes, args.algo, args.quantum)
    print_gantt(intervals)
    for key, value in metrics(processes, intervals).items():
        print(f"{key}: {value:.3f}")


if __name__ == "__main__":
    main()

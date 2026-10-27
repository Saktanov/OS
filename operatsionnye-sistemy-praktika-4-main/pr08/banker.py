#!/usr/bin/env python3
from __future__ import annotations

import argparse


def parse(path: str):
    available = []
    allocation = {}
    maximum = {}
    section = None
    with open(path, encoding="utf-8") as file:
        for raw in file:
            line = raw.strip()
            if not line:
                continue
            parts = line.split()
            if parts[0] == "Available":
                available = list(map(int, parts[1:]))
            elif parts[0] in {"Allocation", "Max"}:
                section = parts[0]
            elif section == "Allocation":
                allocation[parts[0]] = list(map(int, parts[1:]))
            elif section == "Max":
                maximum[parts[0]] = list(map(int, parts[1:]))
    return available, allocation, maximum


def vector_leq(a, b) -> bool:
    return all(x <= y for x, y in zip(a, b))


def vector_add(a, b):
    return [x + y for x, y in zip(a, b)]


def vector_sub(a, b):
    return [x - y for x, y in zip(a, b)]


def safety(available, allocation, maximum):
    need = {pid: vector_sub(maximum[pid], allocation[pid]) for pid in allocation}
    work = available[:]
    finish = {pid: False for pid in allocation}
    sequence = []
    changed = True
    while changed:
        changed = False
        for pid in allocation:
            if not finish[pid] and vector_leq(need[pid], work):
                work = vector_add(work, allocation[pid])
                finish[pid] = True
                sequence.append(pid)
                changed = True
    return all(finish.values()), sequence


def request(available, allocation, maximum, pid, req):
    need = {p: vector_sub(maximum[p], allocation[p]) for p in allocation}
    if not vector_leq(req, need[pid]):
        return False, "request exceeds need"
    if not vector_leq(req, available):
        return False, "not enough available resources"
    new_available = vector_sub(available, req)
    new_allocation = {p: values[:] for p, values in allocation.items()}
    new_allocation[pid] = vector_add(new_allocation[pid], req)
    safe, seq = safety(new_available, new_allocation, maximum)
    if safe:
        return True, "safe: " + " ".join(seq)
    return False, "unsafe, rollback"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--request", nargs=4, metavar=("PID", "A", "B", "C"))
    args = parser.parse_args()
    available, allocation, maximum = parse(args.file)
    safe, sequence = safety(available, allocation, maximum)
    print("SAFE" if safe else "UNSAFE", " ".join(sequence))
    if args.request:
        pid = args.request[0]
        req = list(map(int, args.request[1:]))
        ok, message = request(available, allocation, maximum, pid, req)
        print("GRANTED" if ok else "DENIED", message)


if __name__ == "__main__":
    main()

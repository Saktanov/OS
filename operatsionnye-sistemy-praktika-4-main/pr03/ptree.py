#!/usr/bin/env python3
from __future__ import annotations

import os
from collections import defaultdict
from pathlib import Path


def read_status(pid: str) -> dict[str, str]:
    result = {}
    try:
        for line in Path("/proc", pid, "status").read_text().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                result[key] = value.strip()
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        pass
    return result


uid = os.getuid()
processes = {}
children = defaultdict(list)

for entry in Path("/proc").iterdir():
    if not entry.name.isdigit():
        continue
    status = read_status(entry.name)
    if not status:
        continue
    uid_line = status.get("Uid", "").split()
    if not uid_line or int(uid_line[0]) != uid:
        continue
    pid = int(entry.name)
    ppid = int(status.get("PPid", "0"))
    processes[pid] = {
        "ppid": ppid,
        "name": status.get("Name", "?"),
        "state": status.get("State", "?"),
        "rss": status.get("VmRSS", "0 kB"),
    }
    children[ppid].append(pid)


def show(pid: int, level: int = 0) -> None:
    item = processes[pid]
    print("  " * level + f"{pid} {item['state']} RSS={item['rss']} {item['name']}")
    for child in sorted(children.get(pid, [])):
        show(child, level + 1)


roots = [pid for pid, item in processes.items() if item["ppid"] not in processes]
for root in sorted(roots):
    show(root)

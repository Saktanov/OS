#!/usr/bin/env python3
import os
import sys

if len(sys.argv) != 2:
    print("Usage: python3 hello.py <file>", file=sys.stderr)
    raise SystemExit(1)

path = sys.argv[1]
with open(path, "rb") as file:
    data = file.read()

print(f"{path}: {len(data)} bytes")
print(f"os.stat size: {os.stat(path).st_size} bytes")

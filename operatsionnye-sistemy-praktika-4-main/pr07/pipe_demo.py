#!/usr/bin/env python3
import os

read_fd, write_fd = os.pipe()
pid = os.fork()

if pid == 0:
    os.close(read_fd)
    os.write(write_fd, b"hello from child\n")
    os.close(write_fd)
    os._exit(0)

os.close(write_fd)
data = os.read(read_fd, 1024)
os.close(read_fd)
os.wait()
print(data.decode().strip())

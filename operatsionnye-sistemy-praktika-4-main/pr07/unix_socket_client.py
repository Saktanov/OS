#!/usr/bin/env python3
import socket
import sys

PATH = "/tmp/os_pr07.sock"
expr = " ".join(sys.argv[1:]) or "2 + 2"
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect(PATH)
    client.sendall(expr.encode())
    print(client.recv(1024).decode())

#!/usr/bin/env python3
import os
import socket

PATH = "/tmp/os_pr07.sock"
try:
    os.unlink(PATH)
except FileNotFoundError:
    pass

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
    server.bind(PATH)
    server.listen()
    print("unix socket server started")
    while True:
        conn, _ = server.accept()
        with conn:
            expr = conn.recv(1024).decode().strip()
            if expr == "quit":
                break
            try:
                result = str(eval(expr, {"__builtins__": {}}, {}))
            except Exception as exc:
                result = f"error: {exc}"
            conn.sendall(result.encode())
os.unlink(PATH)

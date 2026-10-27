#!/usr/bin/env python3
import os

REQUEST = "/tmp/os_pr07_request"
RESPONSE = "/tmp/os_pr07_response"
for path in (REQUEST, RESPONSE):
    if not os.path.exists(path):
        os.mkfifo(path)

print("server started")
try:
    while True:
        with open(REQUEST, encoding="utf-8") as request:
            expr = request.read().strip()
        if expr == "quit":
            break
        try:
            result = str(eval(expr, {"__builtins__": {}}, {}))
        except Exception as exc:
            result = f"error: {exc}"
        with open(RESPONSE, "w", encoding="utf-8") as response:
            response.write(result + "\n")
finally:
    for path in (REQUEST, RESPONSE):
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass

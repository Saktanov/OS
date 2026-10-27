#!/usr/bin/env python3
import sys

REQUEST = "/tmp/os_pr07_request"
RESPONSE = "/tmp/os_pr07_response"
expression = " ".join(sys.argv[1:]) or "2 + 2"

with open(REQUEST, "w", encoding="utf-8") as request:
    request.write(expression)
with open(RESPONSE, encoding="utf-8") as response:
    print(response.read().strip())

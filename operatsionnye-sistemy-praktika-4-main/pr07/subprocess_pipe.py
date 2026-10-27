#!/usr/bin/env python3
import subprocess

ls = subprocess.Popen(["ls"], stdout=subprocess.PIPE, text=True)
grep = subprocess.Popen(["grep", "py"], stdin=ls.stdout, stdout=subprocess.PIPE, text=True)
if ls.stdout:
    ls.stdout.close()
output, _ = grep.communicate()
print(output, end="")

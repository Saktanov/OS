#!/usr/bin/env python3
import random

random.seed(42)
with open("numbers.txt", "w", encoding="utf-8") as file:
    for _ in range(1_000_000):
        file.write(str(random.randint(1, 100)) + "\n")
print("numbers.txt created")

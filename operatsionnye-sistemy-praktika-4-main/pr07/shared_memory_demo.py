#!/usr/bin/env python3
import multiprocessing as mp
from multiprocessing import shared_memory
import array

values = array.array("q", range(10_000))
shm = shared_memory.SharedMemory(create=True, size=len(values) * values.itemsize)

def child(name: str, count: int) -> None:
    existing = shared_memory.SharedMemory(name=name)
    data = array.array("q")
    data.frombytes(existing.buf[: count * data.itemsize])
    print("sum in child:", sum(data))
    existing.close()

try:
    shm.buf[: len(values) * values.itemsize] = values.tobytes()
    p = mp.Process(target=child, args=(shm.name, len(values)))
    p.start()
    p.join()
finally:
    shm.close()
    shm.unlink()

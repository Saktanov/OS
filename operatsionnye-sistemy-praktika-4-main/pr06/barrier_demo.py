#!/usr/bin/env python3
import threading

class Barrier:
    def __init__(self, parties: int):
        self.parties = parties
        self.count = 0
        self.generation = 0
        self.condition = threading.Condition()

    def wait(self) -> None:
        with self.condition:
            generation = self.generation
            self.count += 1
            if self.count == self.parties:
                self.generation += 1
                self.count = 0
                self.condition.notify_all()
            else:
                while generation == self.generation:
                    self.condition.wait()

barrier = Barrier(4)

def worker(index: int) -> None:
    for phase in range(3):
        print(f"thread={index} phase={phase}")
        barrier.wait()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

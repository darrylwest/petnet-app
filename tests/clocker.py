#!/usr/bin/env python3
# dpw@plaza.localdomain
# 2023-09-20 20:07:07

import sys
from rich import print
import time
import functools

results = []


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arglst = [repr(arg) for arg in args]
        argstr = ", ".join(arglst)
        msg = f"[{elapsed:0.8f}s] {name}({argstr}) -> {result}"
        results.append(msg)
        print(msg)
        return result

    return clocked


@clock
def snooze(seconds):
    time.sleep(seconds)
    return "ok"


def main(args: list) -> None:
    for n in range(4):
        s = ((n + 1) / 10) + 0.445
        print("*" * 40, f"Calling snooze({s})")
        snooze(s)


if __name__ == "__main__":
    main(sys.argv[1:])

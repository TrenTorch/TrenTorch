from itertools import groupby


def compress_runs(s):
    parts = []
    for ch, run in groupby(s):
        n = sum(1 for _ in run)
        parts.append(ch + (str(n) if n > 1 else ""))
    return "".join(parts)

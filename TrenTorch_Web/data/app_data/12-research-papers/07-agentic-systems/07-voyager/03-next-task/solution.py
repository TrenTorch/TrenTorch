def next_task(done, candidates):
    for t in candidates:
        if t not in done:
            return t
    return None

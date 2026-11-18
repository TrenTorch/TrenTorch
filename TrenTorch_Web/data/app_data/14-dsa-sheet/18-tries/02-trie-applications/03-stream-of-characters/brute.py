def stream_checker(words, stream):
    return [
        any(stream[:i].endswith(w) for w in words) for i in range(1, len(stream) + 1)
    ]

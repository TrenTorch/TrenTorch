def isomorphic_strings(s, t):
    if len(s) != len(t):
        return False
    forward = {}
    backward = {}
    for a, b in zip(s, t):
        if forward.setdefault(a, b) != b or backward.setdefault(b, a) != a:
            return False
    return True

def is_rotation(s, goal):
    if len(s) != len(goal):
        return False
    if not s:
        return True
    return any(s[k:] + s[:k] == goal for k in range(len(s)))

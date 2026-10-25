def smallest_rotation(s):
    return min((s[i:] + s[:i] for i in range(len(s))), default="")

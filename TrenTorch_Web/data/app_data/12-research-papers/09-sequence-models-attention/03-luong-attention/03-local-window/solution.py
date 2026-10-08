def local_window(center, D, T):
    return (max(0, center - D), min(T, center + D + 1))

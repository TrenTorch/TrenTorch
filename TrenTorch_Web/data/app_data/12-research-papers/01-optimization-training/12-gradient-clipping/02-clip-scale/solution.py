def clip_scale(norm, threshold):
    return min(1.0, threshold / norm)

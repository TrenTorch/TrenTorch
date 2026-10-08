def masking_action(u):
    if u < 0.8:
        return "mask"
    if u < 0.9:
        return "random"
    return "keep"

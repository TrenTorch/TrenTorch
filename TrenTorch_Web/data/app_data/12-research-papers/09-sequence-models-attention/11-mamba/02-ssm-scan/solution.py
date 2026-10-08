def ssm_scan(a, b, x):
    h = 0.0
    out = []
    for xt in x:
        h = a * h + b * xt
        out.append(h)
    return out

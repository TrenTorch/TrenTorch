def recurrent_ssm(A_bar, B_bar, C, x):
    h = 0.0
    out = []
    for xt in x:
        h = A_bar * h + B_bar * xt
        out.append(C * h)
    return out

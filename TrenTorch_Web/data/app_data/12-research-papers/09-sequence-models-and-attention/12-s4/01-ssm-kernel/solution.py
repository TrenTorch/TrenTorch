def ssm_kernel(A_bar, B_bar, C, L):
    return [C * (A_bar**k) * B_bar for k in range(L)]

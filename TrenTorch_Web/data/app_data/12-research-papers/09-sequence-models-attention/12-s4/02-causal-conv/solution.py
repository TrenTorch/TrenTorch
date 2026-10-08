def causal_conv_from_kernel(K, x):
    T = len(x)
    return [sum(K[k] * x[t - k] for k in range(min(t, len(K) - 1) + 1)) for t in range(T)]

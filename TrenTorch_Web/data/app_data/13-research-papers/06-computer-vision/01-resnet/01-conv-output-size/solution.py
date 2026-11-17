def conv_output_size(n, k, s, p):
    return (n + 2 * p - k) // s + 1

def causal_padding(kernel, dilation):
    return (kernel - 1) * dilation

def receptive_field(kernels, strides):
    r = 1
    jump = 1
    for k, s in zip(kernels, strides):
        r += (k - 1) * jump
        jump *= s
    return r

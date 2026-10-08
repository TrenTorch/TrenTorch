def tcn_receptive_field(kernel, levels):
    return 1 + (kernel - 1) * (2**levels - 1)

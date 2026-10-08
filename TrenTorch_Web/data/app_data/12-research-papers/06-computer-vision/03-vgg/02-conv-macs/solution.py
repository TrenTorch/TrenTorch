def conv_macs(h, w, c_in, c_out, k=3):
    return h * w * c_in * c_out * k * k

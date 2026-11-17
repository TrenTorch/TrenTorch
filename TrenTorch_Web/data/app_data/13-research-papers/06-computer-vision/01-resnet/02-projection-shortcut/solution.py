def needs_projection(c_in, c_out, stride):
    return c_in != c_out or stride != 1

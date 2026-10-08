def oblivious_leaf_index(bits):
    return sum(int(b) * (2**k) for k, b in enumerate(bits))

def llama_hidden_dim(dim, multiple_of=256):
    hidden = int(2 * 4 * dim / 3)
    return multiple_of * ((hidden + multiple_of - 1) // multiple_of)

def transformer_params(n_layers, d_model, vocab, d_ff=None, tied=True):
    d_ff = 4 * d_model if d_ff is None else d_ff
    per_layer = 4 * d_model ** 2 + 2 * d_model * d_ff
    embedding = vocab * d_model * (1 if tied else 2)
    return n_layers * per_layer + embedding


def training_flops(n_params, n_tokens):
    return 6 * n_params * n_tokens


def chinchilla_tokens(n_params):
    return 20 * n_params

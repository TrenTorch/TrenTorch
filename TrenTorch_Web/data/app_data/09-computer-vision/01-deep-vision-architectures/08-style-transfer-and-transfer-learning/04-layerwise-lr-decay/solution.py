def layer_index(name, n_layers):
    parts = name.split(".")
    if parts[0] == "embed":
        return 0
    if parts[0] == "head":
        return n_layers + 1
    if parts[0] == "layers" and len(parts) > 1 and parts[1].isdigit():
        return int(parts[1]) + 1
    raise ValueError(f"unrecognised parameter name: {name}")


def layerwise_lr(name, n_layers, base_lr, decay):
    return base_lr * decay ** (n_layers + 1 - layer_index(name, n_layers))

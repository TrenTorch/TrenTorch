def wavenet_receptive_field(dilations, kernel=2):
    return 1 + sum((kernel - 1) * d for d in dilations)

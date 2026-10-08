def decoder_inputs(targets, bos):
    return [bos] + list(targets[:-1])

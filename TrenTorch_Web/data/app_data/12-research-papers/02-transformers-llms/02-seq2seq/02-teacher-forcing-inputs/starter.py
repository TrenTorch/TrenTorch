def decoder_inputs(targets, bos):
    """
    targets: the target sentence, a list of tokens
    bos: the begin-of-sentence token

    Returns:
        The decoder's input sequence: bos followed by all targets except the last.
    """
    # TODO: Shift the target sequence right by one, starting with bos (see Theory).
    pass

def local_window(center, D, T):
    """
    center: predicted aligned source position
    D: half-width of the window
    T: source sentence length

    Returns:
        The half-open window (start, end) of source positions to attend to, clipped to the sentence.
    """
    # TODO: Clip the window of width 2D + 1 around center to the sentence bounds (see Theory).
    pass

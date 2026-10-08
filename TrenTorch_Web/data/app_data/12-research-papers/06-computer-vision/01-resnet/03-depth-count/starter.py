def resnet_depth(blocks):
    """
    blocks: number of basic residual blocks in each stage, e.g. [2, 2, 2, 2]

    Returns:
        The nominal depth of the network: the stem convolution, the final fully connected
        layer, and two convolutions per basic block.
    """
    # TODO: Count the stem, the classifier, and two convolutions per block (see Theory).
    pass

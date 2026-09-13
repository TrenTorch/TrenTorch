def linear_flops(batch_size: int, in_features: int, out_features: int, bias: bool = True) -> int:
    """
    Estimate the number of floating-point operations a single forward
    pass through a Linear layer performs.

    Each output element is a dot product over `in_features` inputs: that's
    `in_features` multiplications and `in_features - 1` additions to sum
    them, conventionally rounded up to `in_features` multiply-adds counted
    as 2 FLOPs each (1 multiply + 1 add). There are
    `batch_size * out_features` such output elements. If a bias is added,
    that's one more addition per output element.
    """
    # TODO: multiply_adds = batch_size * in_features * out_features.
    # flops = 2 * multiply_adds. If bias, add batch_size * out_features.
    pass


def conv2d_flops(
    batch_size: int,
    in_channels: int,
    out_channels: int,
    kernel_size: int,
    output_height: int,
    output_width: int,
    bias: bool = True,
) -> int:
    """
    Estimate the number of floating-point operations a single forward
    pass through a (square-kernel, no-groups) Conv2d layer performs.

    Each single output value (one channel, one spatial position, one
    batch element) is a dot product over the kernel's full receptive
    field: `in_channels * kernel_size * kernel_size` multiply-adds. There
    are `batch_size * out_channels * output_height * output_width` such
    output values in total.
    """
    # TODO: output_positions = batch_size * out_channels * output_height
    # * output_width. multiply_adds_per_position = in_channels *
    # kernel_size * kernel_size. flops = 2 * output_positions *
    # multiply_adds_per_position. If bias, add output_positions.
    pass

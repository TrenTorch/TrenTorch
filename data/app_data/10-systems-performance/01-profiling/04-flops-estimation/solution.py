def linear_flops(batch_size: int, in_features: int, out_features: int, bias: bool = True) -> int:
    multiply_adds = batch_size * in_features * out_features
    flops = 2 * multiply_adds
    if bias:
        flops += batch_size * out_features
    return flops


def conv2d_flops(
    batch_size: int,
    in_channels: int,
    out_channels: int,
    kernel_size: int,
    output_height: int,
    output_width: int,
    bias: bool = True,
) -> int:
    output_positions = batch_size * out_channels * output_height * output_width
    multiply_adds_per_position = in_channels * kernel_size * kernel_size
    flops = 2 * output_positions * multiply_adds_per_position
    if bias:
        flops += output_positions
    return flops

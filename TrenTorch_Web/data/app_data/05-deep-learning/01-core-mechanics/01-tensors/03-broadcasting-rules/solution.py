def broadcast_shapes(shape_a: tuple[int, ...], shape_b: tuple[int, ...]) -> tuple[int, ...] | None:
    len_diff = len(shape_a) - len(shape_b)
    if len_diff > 0:
        shape_b = (1,) * len_diff + tuple(shape_b)
    elif len_diff < 0:
        shape_a = (1,) * (-len_diff) + tuple(shape_a)

    result = []
    for dim_a, dim_b in zip(shape_a, shape_b):
        if dim_a == dim_b or dim_a == 1 or dim_b == 1:
            result.append(max(dim_a, dim_b))
        else:
            return None

    return tuple(result)

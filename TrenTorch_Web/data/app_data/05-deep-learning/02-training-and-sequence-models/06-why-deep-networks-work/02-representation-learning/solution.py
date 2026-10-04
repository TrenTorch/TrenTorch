def lookup_table_size(num_features: int) -> int:
    return 2**num_features


def shared_feature_layer_size(num_features: int, num_hidden: int) -> int:
    return num_features * num_hidden + num_hidden


def capacity_ratio(num_features: int, num_hidden: int) -> float:
    return lookup_table_size(num_features) / shared_feature_layer_size(num_features, num_hidden)

def lookup_table_size(num_features: int) -> int:
    """
    The number of entries a pure "lookup table" would need to store one
    output for every possible combination of `num_features` binary
    (present/absent) features, with NO sharing between entries at all.
    """
    pass


def shared_feature_layer_size(num_features: int, num_hidden: int) -> int:
    """
    The number of parameters a single SHARED feature layer needs: a
    (num_features -> num_hidden) linear layer's weight matrix plus its
    bias vector, `[02-layers/01-linear-forward]`-style. This same small
    layer, reused across every possible combination of the underlying
    features, is what a hierarchical/compositional representation relies
    on, instead of a separate stored answer per combination.
    """
    pass


def capacity_ratio(num_features: int, num_hidden: int) -> float:
    """
    How many times BIGGER the lookup table is than the shared feature
    layer, for the same num_features. Demonstrates how fast this gap
    grows as num_features increases.
    """
    pass

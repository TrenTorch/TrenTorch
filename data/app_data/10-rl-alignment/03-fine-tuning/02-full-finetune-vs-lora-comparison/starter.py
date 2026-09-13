ADAM_OPTIMIZER_STATE_BYTES_PER_PARAM = 8  # fp32 momentum + fp32 variance, 4 bytes each


def full_finetune_parameter_count(in_features: int, out_features: int) -> int:
    """
    A full fine-tune of one Linear layer trains EVERY entry of its
    weight matrix, plus its bias: in_features * out_features +
    out_features.
    """
    # TODO: implement
    pass


def lora_parameter_count(in_features: int, out_features: int, rank: int) -> int:
    """
    LoRA trains only its two small matrices (01-lora-low-rank-adapters'
    lora_A: rank x in_features, lora_B: out_features x rank) --
    the frozen base weight/bias contribute zero trainable parameters.
    """
    # TODO: rank * in_features + out_features * rank
    pass


def optimizer_state_bytes(num_trainable_params: int) -> int:
    """
    Adam needs a fp32 momentum AND a fp32 variance value PER
    TRAINABLE parameter (8 bytes total) -- crucially, FROZEN
    parameters need zero optimizer state at all, which is a second,
    separate source of LoRA's memory savings beyond just having fewer
    trainable parameters in the first place.
    """
    # TODO: num_trainable_params * ADAM_OPTIMIZER_STATE_BYTES_PER_PARAM
    pass


def compare_full_finetune_vs_lora(in_features: int, out_features: int, rank: int) -> dict:
    """
    Bundles both parameter-count and optimizer-memory comparisons for
    a single Linear layer, side by side.
    """
    # TODO: compute full_params/lora_params via the two functions
    # above, then return a dict with keys "full_finetune_params",
    # "lora_params", "full_finetune_optimizer_bytes",
    # "lora_optimizer_bytes", "parameter_reduction_factor" (full /
    # lora).
    pass

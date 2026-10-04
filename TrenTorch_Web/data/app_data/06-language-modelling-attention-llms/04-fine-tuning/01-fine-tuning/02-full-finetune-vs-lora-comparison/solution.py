ADAM_OPTIMIZER_STATE_BYTES_PER_PARAM = 8


def full_finetune_parameter_count(in_features: int, out_features: int) -> int:
    return in_features * out_features + out_features


def lora_parameter_count(in_features: int, out_features: int, rank: int) -> int:
    return rank * in_features + out_features * rank


def optimizer_state_bytes(num_trainable_params: int) -> int:
    return num_trainable_params * ADAM_OPTIMIZER_STATE_BYTES_PER_PARAM


def compare_full_finetune_vs_lora(in_features: int, out_features: int, rank: int) -> dict:
    full_params = full_finetune_parameter_count(in_features, out_features)
    lora_params = lora_parameter_count(in_features, out_features, rank)
    return {
        "full_finetune_params": full_params,
        "lora_params": lora_params,
        "full_finetune_optimizer_bytes": optimizer_state_bytes(full_params),
        "lora_optimizer_bytes": optimizer_state_bytes(lora_params),
        "parameter_reduction_factor": full_params / lora_params,
    }

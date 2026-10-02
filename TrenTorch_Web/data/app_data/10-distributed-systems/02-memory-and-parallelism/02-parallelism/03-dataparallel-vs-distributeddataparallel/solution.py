def dp_communication_volume(model_size_bytes: float, num_gpus: int) -> float:
    if num_gpus <= 1:
        return 0.0
    return 2 * (num_gpus - 1) * model_size_bytes

def ddp_communication_volume(model_size_bytes: float, num_gpus: int) -> float:
    if num_gpus <= 1:
        return 0.0
    return 2 * (num_gpus - 1) / num_gpus * model_size_bytes

def dp_gpu0_memory_multiplier(num_gpus: int) -> float:
    return float(num_gpus)

def ddp_gpu0_memory_multiplier(num_gpus: int) -> float:
    return 1.0

def communication_reduction_factor(model_size_bytes: float, num_gpus: int) -> float:
    ddp = ddp_communication_volume(model_size_bytes, num_gpus)
    if ddp == 0.0:
        return 1.0
    return dp_communication_volume(model_size_bytes, num_gpus) / ddp

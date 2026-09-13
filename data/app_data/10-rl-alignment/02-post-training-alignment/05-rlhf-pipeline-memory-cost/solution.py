MODELS_LOADED_SIMULTANEOUSLY = {
    "pretraining": 1,
    "sft": 1,
    "reward_modeling": 1,
    "dpo": 2,
    "ppo": 4,
}


def models_required_for_stage(stage: str) -> int:
    if stage not in MODELS_LOADED_SIMULTANEOUSLY:
        raise ValueError(f"unknown pipeline stage: {stage!r}")
    return MODELS_LOADED_SIMULTANEOUSLY[stage]


def stage_memory_bytes(stage: str, model_size_bytes: float) -> float:
    return models_required_for_stage(stage) * model_size_bytes


def ppo_memory_multiplier_over_sft() -> float:
    return models_required_for_stage("ppo") / models_required_for_stage("sft")


def dpo_memory_multiplier_over_ppo() -> float:
    return models_required_for_stage("dpo") / models_required_for_stage("ppo")

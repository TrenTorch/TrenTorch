MODELS_LOADED_SIMULTANEOUSLY = {
    "pretraining": 1,
    "sft": 1,
    "reward_modeling": 1,
    "dpo": 2,  # policy + frozen reference policy
    "ppo": 4,  # policy + frozen reference policy + reward model + value model
}


def models_required_for_stage(stage: str) -> int:
    """
    How many full model copies must be resident in memory
    SIMULTANEOUSLY for a given stage of the RLHF pipeline. Pretraining,
    SFT, and reward modeling each only ever need the one model being
    trained; DPO additionally needs a frozen reference copy (to keep
    the policy from drifting too far); PPO needs the reference copy
    PLUS the reward model AND a value model (for advantage estimation).
    """
    # TODO: look `stage` up in MODELS_LOADED_SIMULTANEOUSLY, raising
    # ValueError for an unrecognized stage name.
    pass


def stage_memory_bytes(stage: str, model_size_bytes: float) -> float:
    """
    Total memory a stage needs, given how big ONE model copy is.
    """
    # TODO: models_required_for_stage(stage) * model_size_bytes
    pass


def ppo_memory_multiplier_over_sft() -> float:
    """
    How many times more memory PPO needs compared to plain SFT, for
    the SAME base model size.
    """
    # TODO: models_required_for_stage("ppo") /
    # models_required_for_stage("sft")
    pass


def dpo_memory_multiplier_over_ppo() -> float:
    """
    How many times LESS memory DPO needs compared to PPO -- DPO's main
    practical selling point over the full RLHF pipeline.
    """
    # TODO: models_required_for_stage("dpo") /
    # models_required_for_stage("ppo")
    pass

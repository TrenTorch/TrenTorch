VALID_STAGES = {"none", "staging", "production", "archived"}


def create_registry() -> dict:
    return {}


def register_model_version(registry: dict, model_name: str, run_id: str, metrics: dict) -> dict:
    versions = registry.setdefault(model_name, [])
    version_number = len(versions) + 1
    versions.append({"version": version_number, "run_id": run_id, "metrics": dict(metrics), "stage": "none"})
    return registry


def promote_to_stage(registry: dict, model_name: str, version: int, stage: str) -> dict:
    if stage not in VALID_STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    for entry in registry[model_name]:
        if entry["version"] == version:
            entry["stage"] = stage
        elif stage == "production" and entry["stage"] == "production":
            entry["stage"] = "archived"
    return registry


def get_version_at_stage(registry: dict, model_name: str, stage: str) -> dict | None:
    for entry in registry.get(model_name, []):
        if entry["stage"] == stage:
            return entry
    return None

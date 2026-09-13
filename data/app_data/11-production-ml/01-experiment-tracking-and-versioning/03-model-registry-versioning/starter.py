VALID_STAGES = {"none", "staging", "production", "archived"}


def create_registry() -> dict:
    """
    An empty model registry: a mapping from model name to its list of
    registered versions.
    """
    # TODO: return {}
    pass


def register_model_version(registry: dict, model_name: str, run_id: str, metrics: dict) -> dict:
    """
    Registers a new version of a named model, linking it back to the
    experiment run that produced it. Version numbers are assigned
    sequentially per model name, starting at 1, and every new version
    starts in stage "none" (not yet promoted anywhere).
    """
    # TODO: get (or create) the model's version list via
    # registry.setdefault(model_name, []). New version_number =
    # len(existing versions) + 1. Append {"version": version_number,
    # "run_id": run_id, "metrics": dict(metrics), "stage": "none"}.
    # Return registry.
    pass


def promote_to_stage(registry: dict, model_name: str, version: int, stage: str) -> dict:
    """
    Moves a specific version to a new stage. Promoting a version to
    "production" must automatically demote whatever OTHER version was
    previously in "production" down to "archived" -- a real model
    registry never allows two versions to BOTH claim to be the current
    production version at once.
    """
    # TODO: raise ValueError for an unrecognized stage. Otherwise, loop
    # over the model's versions: set the target version's stage to
    # `stage`; if `stage == "production"`, any OTHER version currently
    # at "production" should become "archived". Return registry.
    pass


def get_version_at_stage(registry: dict, model_name: str, stage: str) -> dict | None:
    """
    Returns whichever version of a model currently sits at the given
    stage (e.g. "production"), or None if no version is there.
    """
    # TODO: loop over the model's versions, return the first one whose
    # stage matches; return None if none match.
    pass

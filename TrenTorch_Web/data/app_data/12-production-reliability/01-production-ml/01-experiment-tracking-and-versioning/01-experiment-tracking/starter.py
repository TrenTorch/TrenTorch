def create_run(run_id: str, hyperparameters: dict) -> dict:
    """
    Starts a new tracked run: a record of the run's ID, a COPY of its
    hyperparameters (so later mutating the caller's dict doesn't
    silently corrupt the run's history), and empty containers for
    metrics logged during training and artifacts saved afterward.
    """
    # TODO: return {"run_id": run_id, "hyperparameters": dict(hyperparameters),
    # "metrics": {}, "artifacts": {}}
    pass


def log_metric(run: dict, name: str, value: float, step: int) -> dict:
    """
    Appends one (step, value) measurement to a named metric's history
    -- a metric like "loss" gets logged repeatedly over the course of
    training, once per step, and every one of those measurements
    needs to be kept, not just overwritten by the latest.
    """
    # TODO: run["metrics"].setdefault(name, []).append((step, value)).
    # Return run.
    pass


def log_artifact(run: dict, name: str, path: str) -> dict:
    """
    Records a reference to a saved artifact (a checkpoint file, a
    plot, a config dump) by name -- unlike metrics, artifacts are
    typically saved once, so a later log_artifact call with the same
    name should simply overwrite the earlier reference.
    """
    # TODO: run["artifacts"][name] = path. Return run.
    pass


def get_metric_history(run: dict, name: str) -> list:
    """
    Returns the full list of (step, value) pairs logged for a metric,
    or an empty list if that metric was never logged.
    """
    # TODO: return list(run["metrics"].get(name, []))
    pass


def get_latest_metric(run: dict, name: str) -> float:
    """
    Returns the value logged at the HIGHEST step for a given metric
    (not necessarily the last one APPENDED, if metrics were ever
    logged out of order) -- raises KeyError if the metric was never
    logged at all.
    """
    # TODO: get the metric's history via get_metric_history; if empty,
    # raise KeyError. Otherwise return the value from the entry with
    # the maximum step.
    pass

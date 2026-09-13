def create_run(run_id: str, hyperparameters: dict) -> dict:
    return {"run_id": run_id, "hyperparameters": dict(hyperparameters), "metrics": {}, "artifacts": {}}


def log_metric(run: dict, name: str, value: float, step: int) -> dict:
    run["metrics"].setdefault(name, []).append((step, value))
    return run


def log_artifact(run: dict, name: str, path: str) -> dict:
    run["artifacts"][name] = path
    return run


def get_metric_history(run: dict, name: str) -> list:
    return list(run["metrics"].get(name, []))


def get_latest_metric(run: dict, name: str) -> float:
    history = get_metric_history(run, name)
    if not history:
        raise KeyError(f"no logged values for metric {name!r}")
    return max(history, key=lambda entry: entry[0])[1]

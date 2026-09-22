def build_run_record(
    run_id: str, hyperparameters: list[tuple[str, str]], metrics: list[tuple[str, str]]
) -> dict:
    hp: dict[str, str] = {}
    for key, value in hyperparameters:
        hp[key] = value  # last duplicate wins

    m: dict[str, str] = {}
    for key, value in metrics:
        m[key] = value

    return {
        "run_id": run_id,
        "hyperparameters": dict(sorted(hp.items())),
        "metrics": dict(sorted(m.items())),
    }

def classify_and_store(trajectories: list[tuple[str, bool]]) -> tuple[list[str], list[str]]:
    successful = [trajectory_id for trajectory_id, success in trajectories if success]
    failed = [trajectory_id for trajectory_id, success in trajectories if not success]
    return successful, failed

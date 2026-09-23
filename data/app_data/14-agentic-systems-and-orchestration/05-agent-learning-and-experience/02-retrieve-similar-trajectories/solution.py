def find_similar_trajectories(
    query_tags: set[str], trajectories: list[tuple[str, set[str]]]
) -> list[str]:
    scored = [
        (trajectory_id, len(query_tags & tags)) for trajectory_id, tags in trajectories
    ]
    scored.sort(key=lambda item: (-item[1], item[0]))
    return [trajectory_id for trajectory_id, _overlap in scored]

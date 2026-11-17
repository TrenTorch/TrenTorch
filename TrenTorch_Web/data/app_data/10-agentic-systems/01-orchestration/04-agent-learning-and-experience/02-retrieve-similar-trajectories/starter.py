def find_similar_trajectories(
    query_tags: set[str], trajectories: list[tuple[str, set[str]]]
) -> list[str]:
    """
    query_tags: tags describing the new task at hand.
    trajectories: (trajectory_id, tags) for every stored past run.

    Rank stored trajectories by how many tags they share with
    query_tags (a simple overlap count, not a continuous similarity
    score). Return ALL trajectory ids, sorted by overlap count
    descending, ties broken by ascending id.
    """
    # TODO: Implement the tag-overlap ranking from Theory.
    pass

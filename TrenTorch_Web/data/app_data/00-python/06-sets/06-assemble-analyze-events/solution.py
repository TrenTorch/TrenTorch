def analyze_events(batches: list) -> tuple:
    if not batches:
        return ([], set(), set(), 0)

    unique_ids = []
    seen = set()
    per_batch_sets = []

    for batch in batches:
        batch_set = set(batch)
        per_batch_sets.append(batch_set)
        for event_id in batch:
            if event_id not in seen:
                seen.add(event_id)
                unique_ids.append(event_id)

    common_ids = per_batch_sets[0]
    for batch_set in per_batch_sets[1:]:
        common_ids = common_ids & batch_set

    non_common_ids = {event_id for event_id in seen if event_id not in common_ids}

    return (unique_ids, common_ids, non_common_ids, len(seen))

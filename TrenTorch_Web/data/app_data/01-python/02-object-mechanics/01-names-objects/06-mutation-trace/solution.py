def process_batch(numbers: list, seen: list | None = None) -> dict:
    if seen is None:
        seen = []

    for number in numbers:
        if not number:
            continue
        if number < 0:
            break
        seen.append(number)

    seen_alias = seen

    return {
        "seen": seen,
        "seen_alias_is_same_object": id(seen_alias) == id(seen),
        "count_processed": len(seen),
    }

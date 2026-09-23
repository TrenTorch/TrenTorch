def dedupe_idempotent_calls(call_ids: list[str]) -> list[tuple[str, bool]]:
    seen: set[str] = set()
    result = []
    for call_id in call_ids:
        executed = call_id not in seen
        seen.add(call_id)
        result.append((call_id, executed))
    return result

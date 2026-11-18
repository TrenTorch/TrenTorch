def build_audit_log(actions: list[tuple[str, str, str]]) -> list[str]:
    return [f"[{timestamp}] {actor}: {description}" for timestamp, actor, description in actions]

def route_handoff(current_agent: str, message: str, routing_rules: list[tuple[str, str]]) -> str:
    lowered_message = message.lower()
    for keyword, target_agent in routing_rules:
        if keyword.lower() in lowered_message:
            return target_agent
    return current_agent

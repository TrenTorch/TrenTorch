def process_message_log(messages: list[tuple[str, str, str]]) -> dict[str, tuple[str, str]]:
    state: dict[str, tuple[str, str]] = {}
    for sender, key, value in messages:
        state[key] = (value, sender)
    return state

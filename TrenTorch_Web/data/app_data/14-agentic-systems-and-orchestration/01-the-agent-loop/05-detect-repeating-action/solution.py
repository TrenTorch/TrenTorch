from collections import deque


def detect_repeating_action(
    actions: list[tuple[str, str]], window: int, repeat_threshold: int
) -> int | None:
    recent: deque[tuple[str, str]] = deque(maxlen=window)
    for i, action in enumerate(actions, start=1):
        recent.append(action)
        if recent.count(action) >= repeat_threshold:
            return i
    return None

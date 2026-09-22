def detect_repeating_action(
    actions: list[tuple[str, str]], window: int, repeat_threshold: int
) -> int | None:
    """
    actions: (action, action_input) pairs, one per step, in order.
    window: how many of the most recent steps to consider at any point.
    repeat_threshold: how many times the SAME (action, action_input)
    pair must appear within that sliding window to count as "stuck in
    a loop."

    Walk the steps in order. After each step, look at only the last
    `window` steps seen so far (fewer if not enough steps have
    happened yet) and count how many of them exactly match the action
    just taken. The moment that count reaches repeat_threshold, return
    the current 1-indexed step number. Return None if it never
    happens.
    """
    # TODO: Implement the sliding-window repeat detector from Theory.
    pass

def handle_interrupt_input(current_task: str | None, new_input: str, interrupt_keywords: list[str]) -> str:
    lowered = new_input.lower()
    if any(keyword.lower() in lowered for keyword in interrupt_keywords):
        return "INTERRUPT_AND_SWITCH"
    if current_task is None:
        return "START_NEW_TASK"
    return "QUEUE_AFTER_CURRENT"

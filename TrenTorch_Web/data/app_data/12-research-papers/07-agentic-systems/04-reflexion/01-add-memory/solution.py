def add_reflection(memory, reflection, max_items):
    items = list(memory) + [reflection]
    return items[-max_items:] if max_items > 0 else []

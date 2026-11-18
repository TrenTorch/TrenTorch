def truncate_to_budget(text, max_tokens, head_frac=0.5):
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return text
    head = int(max_tokens * head_frac)
    tail = max_tokens - head
    omitted = len(tokens) - max_tokens
    return " ".join(tokens[:head] + [f"[... {omitted} tokens omitted ...]"] + tokens[len(tokens) - tail:])

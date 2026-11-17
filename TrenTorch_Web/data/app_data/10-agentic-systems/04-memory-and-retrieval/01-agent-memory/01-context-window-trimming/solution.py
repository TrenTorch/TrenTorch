def trim_messages(messages, max_tokens):
    cost = lambda m: len(m["content"].split())
    kept = {i for i, m in enumerate(messages) if m["role"] == "system"}
    total = sum(cost(messages[i]) for i in kept)
    if total > max_tokens:
        raise ValueError("system messages exceed the budget")
    for i in range(len(messages) - 1, -1, -1):
        if i in kept:
            continue
        c = cost(messages[i])
        if total + c > max_tokens:
            break
        kept.add(i)
        total += c
    return [messages[i] for i in sorted(kept)]

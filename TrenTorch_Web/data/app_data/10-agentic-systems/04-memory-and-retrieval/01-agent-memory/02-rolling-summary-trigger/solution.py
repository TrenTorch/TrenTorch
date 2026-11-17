def messages_to_summarize(token_counts, budget, summary_tokens, keep_recent):
    total = sum(token_counts)
    if total <= budget:
        return 0
    max_k = len(token_counts) - keep_recent
    for k in range(1, max_k + 1):
        if sum(token_counts[k:]) + summary_tokens <= budget:
            return k
    raise ValueError("cannot fit within the budget")

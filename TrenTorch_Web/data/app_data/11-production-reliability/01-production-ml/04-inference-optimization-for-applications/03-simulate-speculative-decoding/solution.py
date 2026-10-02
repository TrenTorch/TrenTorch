def simulate_speculative_decoding(
    draft_tokens: list[str], target_tokens: list[str]
) -> tuple[int, list[str]]:
    accepted = 0
    for draft_token, target_token in zip(draft_tokens, target_tokens):
        if draft_token == target_token:
            accepted += 1
        else:
            break

    if accepted < len(target_tokens):
        output = list(target_tokens[: accepted + 1])
    else:
        output = list(target_tokens[:accepted])
    return accepted, output

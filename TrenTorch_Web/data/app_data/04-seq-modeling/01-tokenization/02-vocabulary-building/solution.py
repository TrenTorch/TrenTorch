from collections import Counter


def build_vocabulary(
    token_lists: list[list[str]], min_freq: int = 1, unk_token: str = "<unk>"
) -> dict[str, int]:
    counts = Counter()
    for tokens in token_lists:
        counts.update(tokens)

    vocab = {unk_token: 0}
    for token, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if count >= min_freq:
            vocab[token] = len(vocab)

    return vocab


def encode_with_unk(tokens: list[str], vocab: dict[str, int], unk_token: str = "<unk>") -> list[int]:
    unk_id = vocab[unk_token]
    return [vocab.get(token, unk_id) for token in tokens]

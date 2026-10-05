def solve(tokens, vocab, unk_id):
    """Map each token to its vocabulary ID, using unk_id for unseen tokens."""
    return [vocab.get(token, unk_id) for token in tokens]

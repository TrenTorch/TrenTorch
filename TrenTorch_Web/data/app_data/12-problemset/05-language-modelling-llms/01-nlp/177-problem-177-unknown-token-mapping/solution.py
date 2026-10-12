def solve(tokens, vocab, unk_id):
    return [vocab.get(token, unk_id) for token in tokens]

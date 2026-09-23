def tokenize(vocab: dict[str, int], caption: str) -> list[int]:
    unk_id = 1
    words = caption.split()
    return [vocab.get(word, unk_id) for word in words]

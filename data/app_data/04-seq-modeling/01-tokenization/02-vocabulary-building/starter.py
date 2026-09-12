from collections import Counter


def build_vocabulary(
    token_lists: list[list[str]], min_freq: int = 1, unk_token: str = "<unk>"
) -> dict[str, int]:
    """
    Builds a token -> integer id mapping from a corpus of already-
    tokenized sequences (a list of token lists, `[01-whitespace-char-
    tokenizer]`'s output). `unk_token` is always reserved as id 0.
    Every OTHER token that appears at least `min_freq` times across the
    whole corpus gets its own id, assigned in order of DESCENDING
    frequency (ties broken alphabetically, for a deterministic result).
    """
    counts = Counter()
    for tokens in token_lists:
        counts.update(tokens)
    pass


def encode_with_unk(tokens: list[str], vocab: dict[str, int], unk_token: str = "<unk>") -> list[int]:
    """
    Converts a list of string tokens into their integer ids using
    `vocab`. Any token NOT present in `vocab` (never seen during
    build_vocabulary, or filtered out by min_freq) maps to `unk_token`'s
    id instead of raising an error.
    """
    pass

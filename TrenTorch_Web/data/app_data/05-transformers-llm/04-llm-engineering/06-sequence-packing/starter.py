import numpy as np


def pack_sequences(
    examples: list[list[int]], context_length: int, pad_token: int
) -> tuple[list[list[int]], list[list[int]]]:
    """
    Concatenates every example end-to-end into ONE long stream, then
    chops it into fixed-length chunks of `context_length` (the LAST
    chunk padded with `pad_token` if it's short), filling the model's
    fixed context window far more efficiently than padding every SHORT
    example individually up to `context_length` on its own. Also
    returns, for every packed position, WHICH original example (by
    index into `examples`) it came from (`-1` for padding).
    """
    pass


def build_intra_document_mask(doc_ids: list[int]) -> np.ndarray:
    """
    An additive attention mask preventing a packed sequence's positions
    from attending ACROSS example boundaries: position `i` may attend to
    position `j` only if `j <= i` (ordinary causality) AND `j` belongs to
    the SAME original example as `i` (never a different, unrelated
    example that merely happens to sit nearby after packing). Padding
    positions (`doc_ids == -1`) may attend to nothing.
    """
    pass

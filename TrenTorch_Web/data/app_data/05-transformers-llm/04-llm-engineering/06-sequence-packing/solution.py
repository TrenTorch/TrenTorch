import numpy as np


def pack_sequences(
    examples: list[list[int]], context_length: int, pad_token: int
) -> tuple[list[list[int]], list[list[int]]]:
    all_tokens: list[int] = []
    all_doc_ids: list[int] = []
    for doc_id, example in enumerate(examples):
        all_tokens.extend(example)
        all_doc_ids.extend([doc_id] * len(example))

    packed_sequences = []
    packed_doc_ids = []
    for start in range(0, len(all_tokens), context_length):
        chunk_tokens = all_tokens[start : start + context_length]
        chunk_doc_ids = all_doc_ids[start : start + context_length]

        pad_amount = context_length - len(chunk_tokens)
        if pad_amount > 0:
            chunk_tokens = chunk_tokens + [pad_token] * pad_amount
            chunk_doc_ids = chunk_doc_ids + [-1] * pad_amount

        packed_sequences.append(chunk_tokens)
        packed_doc_ids.append(chunk_doc_ids)

    return packed_sequences, packed_doc_ids


def build_intra_document_mask(doc_ids: list[int]) -> np.ndarray:
    doc_ids_arr = np.array(doc_ids)
    seq_len = len(doc_ids)

    causal_positions = np.arange(seq_len)[None, :] <= np.arange(seq_len)[:, None]
    same_doc = doc_ids_arr[None, :] == doc_ids_arr[:, None]
    not_padding = doc_ids_arr[:, None] != -1

    allowed = causal_positions & same_doc & not_padding
    return np.where(allowed, 0.0, -np.inf)

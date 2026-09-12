"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/06-sequence-packing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
pack_sequences = _module.pack_sequences
build_intra_document_mask = _module.build_intra_document_mask


def test_pack_sequences_concatenates_and_chunks():
    examples = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    # concatenated: [1,2,3,4,5,6,7,8,9], context_length=4 -> 3 chunks (last padded)
    packed, doc_ids = pack_sequences(examples, context_length=4, pad_token=0)
    assert packed == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 0, 0]]


def test_pack_sequences_doc_ids_track_original_example_membership():
    examples = [[1, 2, 3], [4, 5]]
    packed, doc_ids = pack_sequences(examples, context_length=5, pad_token=0)
    assert packed == [[1, 2, 3, 4, 5]]
    assert doc_ids == [[0, 0, 0, 1, 1]]


def test_pack_sequences_pads_the_last_chunk_with_pad_token():
    examples = [[1, 2]]
    packed, doc_ids = pack_sequences(examples, context_length=5, pad_token=99)
    assert packed == [[1, 2, 99, 99, 99]]
    assert doc_ids == [[0, 0, -1, -1, -1]]


def test_pack_sequences_no_padding_needed_when_it_divides_evenly():
    examples = [[1, 2, 3, 4]]
    packed, doc_ids = pack_sequences(examples, context_length=2, pad_token=0)
    assert packed == [[1, 2], [3, 4]]
    assert -1 not in doc_ids[0] and -1 not in doc_ids[1]


def test_intra_document_mask_blocks_attention_across_a_packed_boundary():
    # Positions 0-1 belong to document 0, positions 2-3 to document 1.
    doc_ids = [0, 0, 1, 1]
    mask = build_intra_document_mask(doc_ids)
    # Position 2 (doc 1) must NOT attend to position 0 or 1 (doc 0),
    # even though they're earlier in the packed sequence (causally valid).
    assert mask[2, 0] == -np.inf
    assert mask[2, 1] == -np.inf
    # Position 2 CAN attend to itself (same doc, causal).
    assert mask[2, 2] == 0.0


def test_intra_document_mask_still_respects_ordinary_causality_within_a_document():
    doc_ids = [0, 0, 0]
    mask = build_intra_document_mask(doc_ids)
    assert mask[0, 1] == -np.inf  # position 0 cannot see the future, even within its own document
    assert mask[1, 0] == 0.0  # position 1 CAN see position 0 (past, same document)


def test_intra_document_mask_blocks_padding_positions_from_attending_to_anything():
    doc_ids = [0, 0, -1, -1]
    mask = build_intra_document_mask(doc_ids)
    assert np.all(mask[2, :] == -np.inf)
    assert np.all(mask[3, :] == -np.inf)


def test_intra_document_mask_shape():
    doc_ids = [0, 0, 1, 1, 1]
    mask = build_intra_document_mask(doc_ids)
    assert mask.shape == (5, 5)


def test_naive_causal_masking_alone_would_wrongly_allow_cross_document_attention():
    # Demonstrates WHY this mask is needed: an ordinary causal mask
    # (ignoring document boundaries) would allow position 2 to attend to
    # position 0, even though they belong to different, unrelated
    # documents that merely happen to sit next to each other after packing.
    doc_ids = [0, 0, 1, 1]
    mask = build_intra_document_mask(doc_ids)
    ordinary_causal_would_allow = 2 >= 0  # position 2 >= position 0, causally valid
    assert ordinary_causal_would_allow  # sanity: causal alone doesn't block it
    assert mask[2, 0] == -np.inf  # but the intra-document mask correctly does

"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
import pytest

make_pairs = _module.make_pairs
DOCS = [["a1", "a2", "a3"], ["b1", "b2"], ["c1", "c2", "c3"]]


def test_1_replays_the_stated_stream():
    got = make_pairs(DOCS, np.random.RandomState(4))
    r = np.random.RandomState(4)
    exp = []
    for i, doc in enumerate(DOCS):
        others = [s for j, d in enumerate(DOCS) if j != i for s in d]
        for k in range(len(doc) - 1):
            if r.random_sample() < 0.5:
                exp.append((doc[k], doc[k + 1], 1))
            else:
                exp.append((doc[k], others[r.randint(len(others))], 0))
    assert got == exp


def test_2_number_of_pairs_is_sentences_minus_documents():
    assert len(make_pairs(DOCS, np.random.RandomState(0))) == 2 + 1 + 2


def test_3_positive_pairs_are_true_continuations():
    for a, b, y in make_pairs(DOCS * 5, np.random.RandomState(1)):
        if y == 1:
            assert (a, b) in {("a1", "a2"), ("a2", "a3"), ("b1", "b2"), ("c1", "c2"), ("c2", "c3")}


def test_4_negatives_come_from_a_different_document():
    docs = [[f"{c}{k}" for k in range(5)] for c in "abcd"]
    negatives = [(a, b) for a, b, y in make_pairs(docs, np.random.RandomState(2)) if y == 0]
    assert negatives and all(a[0] != b[0] for a, b in negatives)


def test_5_labels_are_roughly_balanced():
    docs = [[f"d{i}s{k}" for k in range(50)] for i in range(4)]
    labels = [y for _, _, y in make_pairs(docs, np.random.RandomState(0))]
    assert abs(np.mean(labels) - 0.5) < 0.1


def test_6_single_document_raises():
    with pytest.raises(ValueError):
        make_pairs([["a", "b"]], np.random.RandomState(0))


def test_7_input_untouched():
    snap = [list(d) for d in DOCS]
    make_pairs(DOCS, np.random.RandomState(0))
    assert DOCS == snap

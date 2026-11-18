"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
transfer_weights = _module.transfer_weights


def make():
    src = {"backbone.w": np.ones((3, 3)), "backbone.b": np.ones(3), "head.w": np.ones((1000, 3)), "extra.w": np.ones(2)}
    dst = {"backbone.w": np.zeros((3, 3)), "backbone.b": np.zeros(3), "head.w": np.zeros((10, 3)), "new.w": np.zeros(4)}
    return src, dst


def test_1_matching_tensors_are_copied():
    out, copied, _ = transfer_weights(*make())
    assert copied == ["backbone.b", "backbone.w"] and np.all(out["backbone.w"] == 1.0)


def test_2_resized_head_is_skipped_and_keeps_its_initialization():
    out, _, skipped = transfer_weights(*make())
    assert "head.w" in skipped and out["head.w"].shape == (10, 3) and np.all(out["head.w"] == 0.0)


def test_3_names_missing_from_the_source_are_skipped():
    _, _, skipped = transfer_weights(*make())
    assert skipped == ["head.w", "new.w"]


def test_4_names_only_in_the_source_are_ignored():
    out, _, _ = transfer_weights(*make())
    assert "extra.w" not in out and set(out) == {"backbone.w", "backbone.b", "head.w", "new.w"}


def test_5_returned_arrays_are_independent_copies():
    src, dst = make()
    out, _, _ = transfer_weights(src, dst)
    out["backbone.w"][0, 0] = 99.0
    assert src["backbone.w"][0, 0] == 1.0 and dst["backbone.w"][0, 0] == 0.0


def test_6_inputs_are_not_modified():
    src, dst = make()
    ss = {k: v.copy() for k, v in src.items()}
    sd = {k: v.copy() for k, v in dst.items()}
    transfer_weights(src, dst)
    assert all(np.array_equal(src[k], ss[k]) for k in src) and all(np.array_equal(dst[k], sd[k]) for k in dst)


def test_7_identical_models_copy_everything():
    src, _ = make()
    _, copied, skipped = transfer_weights(src, {k: np.zeros_like(v) for k, v in src.items()})
    assert skipped == [] and copied == sorted(src)

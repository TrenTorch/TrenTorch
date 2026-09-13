"""
pytest data/app_data/08-systems-performance/01-profiling/05-checkpointing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/01-profiling/{Path(__file__).resolve().parent.name}")
save_checkpoint = _module.save_checkpoint
load_checkpoint = _module.load_checkpoint


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_round_trip_preserves_parameter_values(tmp_path):
    params = {"w": np.array([[1.0, 2.0], [3.0, 4.0]])}
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint(params, epoch=3, path=path)
    loaded_params, loaded_epoch = load_checkpoint(path)
    assert np.array_equal(loaded_params["w"], params["w"])
    assert loaded_epoch == 3


def test_02_round_trip_preserves_multiple_named_parameters(tmp_path):
    params = {"layer1.weight": np.zeros((3, 3)), "layer1.bias": np.ones(3)}
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint(params, epoch=0, path=path)
    loaded_params, _ = load_checkpoint(path)
    assert set(loaded_params.keys()) == {"layer1.weight", "layer1.bias"}
    assert np.array_equal(loaded_params["layer1.weight"], params["layer1.weight"])
    assert np.array_equal(loaded_params["layer1.bias"], params["layer1.bias"])


# --- Shape / general-case coverage -----------------------------------


def test_03_epoch_round_trips_as_a_plain_int(tmp_path):
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint({"w": np.zeros(2)}, epoch=17, path=path)
    _, loaded_epoch = load_checkpoint(path)
    assert isinstance(loaded_epoch, int)
    assert loaded_epoch == 17


def test_04_arrays_of_different_shapes_and_dtypes_all_round_trip(tmp_path):
    params = {
        "scalar": np.array(5.0),
        "vector": np.arange(5, dtype=np.float64),
        "matrix": np.eye(3, dtype=np.float32),
    }
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint(params, epoch=1, path=path)
    loaded, _ = load_checkpoint(path)
    for key in params:
        assert np.array_equal(loaded[key], params[key])


# --- Parameter handling -------------------------------------------------


def test_05_two_different_checkpoints_do_not_interfere_with_each_other(tmp_path):
    path_a = str(tmp_path / "a.npz")
    path_b = str(tmp_path / "b.npz")
    save_checkpoint({"w": np.zeros(2)}, epoch=1, path=path_a)
    save_checkpoint({"w": np.ones(2)}, epoch=2, path=path_b)

    loaded_a, epoch_a = load_checkpoint(path_a)
    loaded_b, epoch_b = load_checkpoint(path_b)
    assert np.array_equal(loaded_a["w"], np.zeros(2))
    assert np.array_equal(loaded_b["w"], np.ones(2))
    assert epoch_a == 1
    assert epoch_b == 2


# --- Edge cases ---------------------------------------------------------


def test_06_empty_parameter_dict_still_round_trips_the_epoch(tmp_path):
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint({}, epoch=42, path=path)
    loaded_params, loaded_epoch = load_checkpoint(path)
    assert loaded_params == {}
    assert loaded_epoch == 42


def test_07_epoch_zero_is_not_confused_with_a_missing_epoch(tmp_path):
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint({"w": np.zeros(1)}, epoch=0, path=path)
    _, loaded_epoch = load_checkpoint(path)
    assert loaded_epoch == 0


# --- Array hygiene ------------------------------------------------------


def test_08_does_not_mutate_the_input_params_dict(tmp_path):
    params = {"w": np.array([1.0, 2.0])}
    params_copy = {"w": params["w"].copy()}
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint(params, epoch=0, path=path)
    assert np.array_equal(params["w"], params_copy["w"])


# --- Independent correctness oracle -----------------------------------


def test_09_the_saved_file_is_a_real_loadable_npz_archive(tmp_path):
    # Verifies save_checkpoint actually produces a standard NumPy .npz
    # archive (not some ad-hoc format), by reading it back with plain
    # np.load directly, independent of load_checkpoint's own logic.
    path = str(tmp_path / "ckpt.npz")
    save_checkpoint({"w": np.array([9.0, 8.0])}, epoch=5, path=path)
    with np.load(path) as raw:
        assert "w" in raw.files
        assert np.array_equal(raw["w"], np.array([9.0, 8.0]))

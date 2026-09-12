"""
pytest data/app_data/03-dl-training/03-training-loop/03-train-eval-mode/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/03-training-loop/{Path(__file__).resolve().parent.name}")
TrainableModule = _module.TrainableModule


def test_defaults_to_training_mode():
    m = TrainableModule()
    assert m.training is True


def test_eval_sets_training_to_false():
    m = TrainableModule()
    m.eval()
    assert m.training is False


def test_train_with_no_arguments_sets_training_to_true():
    m = TrainableModule()
    m.eval()
    m.train()
    assert m.training is True


def test_train_with_explicit_false_behaves_like_eval():
    m = TrainableModule()
    m.train(False)
    assert m.training is False


def test_train_and_eval_return_self_for_chaining():
    m = TrainableModule()
    result = m.train()
    assert result is m
    result2 = m.eval()
    assert result2 is m


def test_eval_propagates_to_a_single_child_module():
    parent = TrainableModule()
    child = TrainableModule()
    parent.register_module("layer1", child)
    parent.eval()
    assert parent.training is False
    assert child.training is False


def test_eval_propagates_through_multiple_levels_of_nesting():
    grandparent = TrainableModule()
    parent = TrainableModule()
    child = TrainableModule()
    parent.register_module("mid", child)
    grandparent.register_module("top", parent)
    grandparent.eval()
    assert grandparent.training is False
    assert parent.training is False
    assert child.training is False


def test_train_after_eval_flips_every_level_back_to_true():
    parent = TrainableModule()
    child = TrainableModule()
    parent.register_module("layer1", child)
    parent.eval()
    parent.train()
    assert parent.training is True
    assert child.training is True


def test_sibling_children_are_all_updated():
    parent = TrainableModule()
    child1 = TrainableModule()
    child2 = TrainableModule()
    parent.register_module("a", child1)
    parent.register_module("b", child2)
    parent.eval()
    assert child1.training is False
    assert child2.training is False


def test_train_propagates_to_children_not_just_sets_the_top_level_flag():
    # Directly targets a mutant that sets self.training but forgets to
    # recurse into self._modules at all: a child module's training flag
    # would then never change, silently leaving e.g. a Dropout layer
    # buried inside a larger model stuck in training mode forever, even
    # after the top-level model.eval() call.
    grandparent = TrainableModule()
    parent = TrainableModule()
    child = TrainableModule()
    parent.register_module("mid", child)
    grandparent.register_module("top", parent)
    grandparent.eval()
    assert child.training is False

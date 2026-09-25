"""
pytest data/app_data/02-math-and-statistics/08-probability-foundations/06-chain-rule-of-probability/tests.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/08-probability-foundations/06-chain-rule-of-probability")
joint_via_chain_rule = _module.joint_via_chain_rule
chain_rule_general = _module.chain_rule_general


# ---- 1-2: basic correctness ----


def test_1_three_variable_joint():
    result = joint_via_chain_rule(0.5, 0.4, 0.2)
    assert math.isclose(result, 0.04)


def test_2_general_chain_matches_the_three_variable_case():
    result = chain_rule_general([0.5, 0.4, 0.2])
    assert math.isclose(result, joint_via_chain_rule(0.5, 0.4, 0.2))


# ---- shape / general-case coverage ----


def test_3_general_chain_with_five_variables():
    conditionals = [0.9, 0.5, 0.5, 0.8, 0.3]
    expected = 0.9 * 0.5 * 0.5 * 0.8 * 0.3
    result = chain_rule_general(conditionals)
    assert math.isclose(result, expected)


def test_4_certain_first_variable_leaves_the_rest_unchanged():
    result = joint_via_chain_rule(1.0, 0.6, 0.7)
    assert math.isclose(result, 0.42)


# ---- edge cases ----


def test_5_single_variable_chain_is_just_its_own_probability():
    result = chain_rule_general([0.37])
    assert math.isclose(result, 0.37)


def test_6_any_zero_probability_factor_makes_the_whole_joint_zero():
    result = joint_via_chain_rule(0.5, 0.0, 0.9)
    assert result == 0.0


def test_7_all_probability_one_factors_give_a_joint_of_one():
    result = chain_rule_general([1.0, 1.0, 1.0])
    assert math.isclose(result, 1.0)


# ---- mutation-catching ----


def test_8_chain_rule_multiplies_not_adds():
    # A wrong implementation adding the factors would give 1.1 instead
    # of the correct 0.06 for these inputs.
    result = joint_via_chain_rule(0.5, 0.3, 0.4)
    assert math.isclose(result, 0.06)
    assert not math.isclose(result, 1.2)


def test_9_general_chain_uses_every_factor_not_just_the_first_and_last():
    # A wrong implementation multiplying only conditionals[0]*conditionals[-1]
    # would ignore the middle factor and give a different result.
    result = chain_rule_general([0.5, 0.2, 0.9])
    assert math.isclose(result, 0.09)
    assert not math.isclose(result, 0.45)


# ---- independent oracle ----


def test_10_matches_a_hand_computed_reference_case():
    # P(X)=0.6, P(Y|X)=0.3, P(Z|X,Y)=0.9 -> joint = 0.6*0.3*0.9 = 0.162
    result = joint_via_chain_rule(0.6, 0.3, 0.9)
    assert math.isclose(result, 0.162)
    assert math.isclose(chain_rule_general([0.6, 0.3, 0.9]), 0.162)

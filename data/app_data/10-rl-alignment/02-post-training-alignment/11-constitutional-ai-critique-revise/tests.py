"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/11-constitutional-ai-critique-revise/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
apply_critique_revision_step = _module.apply_critique_revision_step
constitutional_ai_pipeline = _module.constitutional_ai_pipeline


def _critique_if_contains(bad_word):
    def critique_fn(response, principle):
        if bad_word in response:
            return f"response contains '{bad_word}', violating {principle}"
        return None

    return critique_fn


def _replace_word(bad_word, replacement):
    def revise_fn(response, critique):
        return response.replace(bad_word, replacement)

    return revise_fn


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_no_violation_leaves_response_unchanged():
    critique_fn = _critique_if_contains("rude")
    revise_fn = _replace_word("rude", "polite")
    result = apply_critique_revision_step("a perfectly nice response", "be polite", critique_fn, revise_fn)
    assert result["response"] == "a perfectly nice response"
    assert result["revised"] is False
    assert result["critique"] is None


def test_02_violation_triggers_a_revision():
    critique_fn = _critique_if_contains("rude")
    revise_fn = _replace_word("rude", "polite")
    result = apply_critique_revision_step("that was a rude thing to say", "be polite", critique_fn, revise_fn)
    assert result["response"] == "that was a polite thing to say"
    assert result["revised"] is True
    assert result["critique"] is not None


# --- General-case coverage --------------------------------------------


def test_03_pipeline_applies_multiple_principles_in_order():
    def critique_fn(response, principle):
        if principle in response:
            return f"violates {principle}"
        return None

    def revise_fn(response, critique):
        # Fixes only the SPECIFIC word the critique flagged, not every
        # possible violation at once -- matching a real critique/revise
        # step, which addresses one identified problem at a time.
        violated_word = critique.removeprefix("violates ")
        return response.replace(violated_word, "good")

    result = constitutional_ai_pipeline("a mean and unsafe response", ["mean", "unsafe"], critique_fn, revise_fn)
    assert "mean" not in result["final_response"]
    assert "unsafe" not in result["final_response"]
    assert len(result["critiques_applied"]) == 2


def test_04_pipeline_records_no_critiques_when_nothing_violates():
    critique_fn = lambda response, principle: None
    revise_fn = lambda response, critique: response
    result = constitutional_ai_pipeline("a fine response", ["p1", "p2", "p3"], critique_fn, revise_fn)
    assert result["final_response"] == "a fine response"
    assert result["critiques_applied"] == []


def test_05_later_principle_sees_the_already_revised_response():
    calls = []

    def critique_fn(response, principle):
        calls.append(response)
        if principle == "no-x" and "x" in response:
            return "has x"
        return None

    def revise_fn(response, critique):
        return response.replace("x", "")

    constitutional_ai_pipeline("x-y-x", ["no-x", "no-x"], critique_fn, revise_fn)
    # Second call to critique_fn must see the ALREADY-revised response
    # (all "x"s removed), not the original.
    assert calls[1] == "-y-"


# --- Parameter handling -------------------------------------------------


def test_06_critiques_applied_preserves_order():
    def critique_fn(response, principle):
        return f"issue: {principle}"

    def revise_fn(response, critique):
        return response + "!"

    result = constitutional_ai_pipeline("start", ["first", "second", "third"], critique_fn, revise_fn)
    assert result["critiques_applied"] == ["issue: first", "issue: second", "issue: third"]


def test_07_final_response_reflects_all_applied_revisions():
    def critique_fn(response, principle):
        return "always revise"

    def revise_fn(response, critique):
        return response + "+"

    result = constitutional_ai_pipeline("base", ["p1", "p2", "p3"], critique_fn, revise_fn)
    assert result["final_response"] == "base+++"


# --- Edge cases ---------------------------------------------------------


def test_08_empty_principles_list_returns_response_unchanged():
    critique_fn = lambda r, p: "should never be called"
    revise_fn = lambda r, c: "should never be called"
    result = constitutional_ai_pipeline("unchanged", [], critique_fn, revise_fn)
    assert result["final_response"] == "unchanged"
    assert result["critiques_applied"] == []


def test_09_single_principle_pipeline_matches_single_step():
    critique_fn = _critique_if_contains("bad")
    revise_fn = _replace_word("bad", "good")
    step = apply_critique_revision_step("a bad response", "be good", critique_fn, revise_fn)
    pipeline_result = constitutional_ai_pipeline("a bad response", ["be good"], critique_fn, revise_fn)
    assert pipeline_result["final_response"] == step["response"]


# --- Independent correctness oracle -----------------------------------


def test_10_critiques_applied_only_includes_actually_triggered_critiques():
    # Directly targets a mutant that appends EVERY principle's
    # critique_fn result regardless of whether it was None (e.g.
    # appending None itself, or always treating a response as
    # revised) -- only genuinely triggered revisions should appear.
    def critique_fn(response, principle):
        return "triggered" if principle == "strict" else None

    def revise_fn(response, critique):
        return response + "[revised]"

    result = constitutional_ai_pipeline("base", ["lenient", "strict", "lenient"], critique_fn, revise_fn)
    assert result["critiques_applied"] == ["triggered"]
    assert result["final_response"] == "base[revised]"

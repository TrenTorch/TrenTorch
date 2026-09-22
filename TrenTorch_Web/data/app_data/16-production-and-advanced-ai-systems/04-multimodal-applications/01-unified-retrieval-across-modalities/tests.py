"""pytest data/app_data/16-production-and-advanced-ai-systems/04-multimodal-applications/01-unified-retrieval-across-modalities/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

retrieve_across_modalities = load_solution(
    f"16-production-and-advanced-ai-systems/04-multimodal-applications/{Path(__file__).resolve().parent.name}"
).retrieve_across_modalities


def test_1_ranks_by_keyword_match_count():
    chunks = [
        ("c1", "text", "a report about quarterly revenue growth"),
        ("c2", "image_caption", "a chart showing revenue"),
        ("c3", "text", "an unrelated recipe for bread"),
    ]
    result = retrieve_across_modalities(chunks, ["revenue", "growth"])
    assert result == ["c1", "c2"]


def test_2_image_caption_and_text_scored_identically():
    chunks = [
        ("c1", "image_caption", "revenue growth chart"),
        ("c2", "text", "revenue growth report"),
    ]
    result = retrieve_across_modalities(chunks, ["revenue", "growth"])
    assert result == ["c1", "c2"]


def test_3_zero_score_chunks_excluded():
    chunks = [("c1", "text", "revenue up"), ("c2", "text", "totally unrelated")]
    assert retrieve_across_modalities(chunks, ["revenue"]) == ["c1"]


def test_4_case_insensitive_matching():
    chunks = [("c1", "text", "REVENUE Growth")]
    assert retrieve_across_modalities(chunks, ["revenue", "growth"]) == ["c1"]


def test_5_tie_in_score_preserves_original_order():
    chunks = [("c1", "text", "revenue"), ("c2", "image_caption", "revenue")]
    assert retrieve_across_modalities(chunks, ["revenue"]) == ["c1", "c2"]


def test_6_no_matches_returns_empty_list():
    chunks = [("c1", "text", "nothing relevant here")]
    assert retrieve_across_modalities(chunks, ["revenue"]) == []

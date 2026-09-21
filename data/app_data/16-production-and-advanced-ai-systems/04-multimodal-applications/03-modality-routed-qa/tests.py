"""pytest data/app_data/16-production-and-advanced-ai-systems/04-multimodal-applications/03-modality-routed-qa/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

route_modality_for_question = load_solution(
    f"16-production-and-advanced-ai-systems/04-multimodal-applications/{Path(__file__).resolve().parent.name}"
).route_modality_for_question


MODALITY_KEYWORDS = {
    "image": ["picture", "photo", "chart", "image"],
    "table": ["table", "row", "column", "spreadsheet"],
}


def test_1_matches_image_keyword():
    assert route_modality_for_question("what does the chart show?", MODALITY_KEYWORDS, "text") == "image"


def test_2_matches_table_keyword():
    assert route_modality_for_question(
        "what's in the third row of the table?", MODALITY_KEYWORDS, "text"
    ) == "table"


def test_3_no_match_returns_default():
    assert route_modality_for_question("what is the capital of France?", MODALITY_KEYWORDS, "text") == (
        "text"
    )


def test_4_case_insensitive_match():
    assert route_modality_for_question("Show me the PHOTO", MODALITY_KEYWORDS, "text") == "image"


def test_5_first_matching_modality_in_dict_order_wins():
    # contains both an image keyword ("chart") and a table keyword ("row") --
    # "image" is declared first in MODALITY_KEYWORDS, so it wins.
    assert route_modality_for_question(
        "compare the chart to the table's row values", MODALITY_KEYWORDS, "text"
    ) == "image"

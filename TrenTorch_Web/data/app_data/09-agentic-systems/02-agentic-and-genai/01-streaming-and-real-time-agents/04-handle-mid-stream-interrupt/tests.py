"""pytest tests.py"""

from _load import load_solution

handle_interrupt_input = load_solution(__file__).handle_interrupt_input


KEYWORDS = ["stop", "cancel", "never mind"]


def test_1_interrupt_keyword_while_task_running():
    assert handle_interrupt_input("summarizing document", "stop, forget it", KEYWORDS) == "INTERRUPT_AND_SWITCH"


def test_2_interrupt_keyword_is_case_insensitive():
    assert handle_interrupt_input("summarizing document", "CANCEL that", KEYWORDS) == "INTERRUPT_AND_SWITCH"


def test_3_no_keyword_and_no_current_task():
    assert handle_interrupt_input(None, "what's the weather", KEYWORDS) == "START_NEW_TASK"


def test_4_no_keyword_but_task_running():
    assert handle_interrupt_input("summarizing document", "also check my calendar", KEYWORDS) == (
        "QUEUE_AFTER_CURRENT"
    )


def test_5_interrupt_keyword_takes_priority_even_when_idle():
    assert handle_interrupt_input(None, "never mind", KEYWORDS) == "INTERRUPT_AND_SWITCH"

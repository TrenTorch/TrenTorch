import re
import string
from collections import Counter


def normalize_answer(s: str) -> str:
    """Lowercase, remove punctuation, drop articles a/an/the, collapse whitespace."""
    # TODO
    pass


def exact_match(prediction: str, golds: list[str]) -> float:
    """1.0 if the normalised prediction equals any normalised gold answer."""
    # TODO
    pass


def token_f1(prediction: str, gold: str) -> float:
    """Token-overlap F1 between normalised strings (multiset intersection)."""
    # TODO
    pass

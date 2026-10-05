"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
luhn_valid = _module.luhn_valid
redact_pii = _module.redact_pii


def test_1_luhn_known_numbers():
    assert luhn_valid("4111111111111111") and luhn_valid("5500005555555559")
    assert not luhn_valid("4111111111111112")


def test_2_luhn_length_and_non_digit_rules():
    assert not luhn_valid("12345") and not luhn_valid("4111-1111-1111-1111") and not luhn_valid("1" * 20)


def test_3_email_and_phone():
    out, counts = redact_pii("Mail jo.doe+x@example.co.uk or call 555-123-4567.")
    assert out == "Mail [EMAIL] or call [PHONE]." and counts == {"EMAIL": 1, "PHONE": 1}


def test_4_ssn():
    out, counts = redact_pii("SSN 123-45-6789 on file")
    assert out == "SSN [SSN] on file" and counts == {"SSN": 1}


def test_5_valid_card_with_separators_is_redacted_but_random_digits_are_not():
    out, counts = redact_pii("Card 4111 1111 1111 1111 and order 4111 1111 1111 1112")
    assert out == "Card [CARD] and order 4111 1111 1111 1112" and counts == {"CARD": 1}


def test_6_counts_include_every_replacement_and_nothing_else():
    out, counts = redact_pii("a@b.com, c@d.org and 555.222.3333")
    assert counts == {"EMAIL": 2, "PHONE": 1} and "@" not in out


def test_7_clean_text_unchanged():
    assert redact_pii("Nothing to see here: 42 items.") == ("Nothing to see here: 42 items.", {})

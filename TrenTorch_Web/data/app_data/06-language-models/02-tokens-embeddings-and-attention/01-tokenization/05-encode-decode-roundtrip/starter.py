
from _load import load_solution

whitespace_tokenize = load_solution("seq-tokenization-whitespace-char").whitespace_tokenize
_vocab_module = load_solution("seq-tokenization-vocabulary-building")
encode_with_unk = _vocab_module.encode_with_unk


def encode(text: str, vocab: dict[str, int], unk_token: str = "<unk>") -> list[int]:
    """
    The full text-to-ids pipeline: tokenize `text` (reusing
    `[01-whitespace-char-tokenizer]`'s whitespace_tokenize), then convert
    the resulting tokens to ids (reusing `[02-vocabulary-building]`'s
    encode_with_unk).
    """
    pass


def build_inverse_vocab(vocab: dict[str, int]) -> dict[int, str]:
    """Builds the REVERSE mapping: id -> token, from vocab's token -> id."""
    pass


def decode(ids: list[int], vocab: dict[str, int]) -> str:
    """
    The full ids-to-text pipeline: converts each id back to its token
    (via build_inverse_vocab) and joins them with single spaces back into
    one string.
    """
    pass

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

whitespace_tokenize = load_solution(
    "04-seq-modeling/01-tokenization/01-whitespace-char-tokenizer"
).whitespace_tokenize
_vocab_module = load_solution("04-seq-modeling/01-tokenization/02-vocabulary-building")
encode_with_unk = _vocab_module.encode_with_unk


def encode(text: str, vocab: dict[str, int], unk_token: str = "<unk>") -> list[int]:
    tokens = whitespace_tokenize(text)
    return encode_with_unk(tokens, vocab, unk_token)


def build_inverse_vocab(vocab: dict[str, int]) -> dict[int, str]:
    return {token_id: token for token, token_id in vocab.items()}


def decode(ids: list[int], vocab: dict[str, int]) -> str:
    inverse_vocab = build_inverse_vocab(vocab)
    tokens = [inverse_vocab[token_id] for token_id in ids]
    return " ".join(tokens)

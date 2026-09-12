import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_bpe_module = load_solution("04-seq-modeling/01-tokenization/03-bpe-single-merge")
bpe_single_merge_step = _bpe_module.bpe_single_merge_step
merge_pair = _bpe_module.merge_pair


def train_bpe(corpus: list[list[str]], num_merges: int) -> tuple[list[list[str]], list[tuple[str, str]]]:
    merges = []
    for _ in range(num_merges):
        corpus, merged_pair = bpe_single_merge_step(corpus)
        merges.append(merged_pair)
    return corpus, merges


def apply_merges(tokens: list[str], merges: list[tuple[str, str]]) -> list[str]:
    for pair in merges:
        tokens = merge_pair([tokens], pair)[0]
    return tokens

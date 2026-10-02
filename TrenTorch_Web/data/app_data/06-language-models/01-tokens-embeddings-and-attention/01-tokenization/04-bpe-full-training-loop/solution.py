
from _load import load_solution

_bpe_module = load_solution("seq-tokenization-bpe-single-merge")
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

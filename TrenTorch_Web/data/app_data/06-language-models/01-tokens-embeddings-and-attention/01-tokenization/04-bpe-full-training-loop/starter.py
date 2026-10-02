
from _load import load_solution

_bpe_module = load_solution("seq-tokenization-bpe-single-merge")
bpe_single_merge_step = _bpe_module.bpe_single_merge_step
merge_pair = _bpe_module.merge_pair


def train_bpe(corpus: list[list[str]], num_merges: int) -> tuple[list[list[str]], list[tuple[str, str]]]:
    """
    Runs `[03-bpe-single-merge]`'s bpe_single_merge_step repeatedly,
    `num_merges` times, building up a full BPE merge vocabulary. Returns
    the final corpus (fully merged, `num_merges` times) and the ORDERED
    list of every pair merged along the way, in the exact order they
    were learned (this order matters: apply_merges below has to replay
    them in the SAME order to correctly tokenize new text later).
    """
    pass


def apply_merges(tokens: list[str], merges: list[tuple[str, str]]) -> list[str]:
    """
    Applies a previously-learned list of merges (from train_bpe) to a
    NEW, single sequence of character-level tokens, in the SAME order
    they were originally learned, this is how a trained BPE tokenizer
    encodes text it wasn't trained on.
    """
    pass

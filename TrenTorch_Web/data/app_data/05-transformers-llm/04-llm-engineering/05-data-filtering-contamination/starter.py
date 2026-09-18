def get_ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    """
    Every contiguous `n`-token window in `tokens`, as a SET of tuples
    (duplicates collapse; only distinct n-grams matter).
    """
    pass


def has_contamination(train_doc_tokens: list[str], eval_ngrams: set[tuple[str, ...]], n: int) -> bool:
    """
    `True` if `train_doc_tokens` shares ANY `n`-gram with `eval_ngrams`
    (a set of n-grams drawn from the evaluation set), the signal that
    this training document may leak evaluation content.
    """
    pass


def filter_contaminated_documents(
    train_documents: list[list[str]], eval_documents: list[list[str]], n: int
) -> list[int]:
    """
    Builds the full set of `n`-grams appearing ANYWHERE in
    `eval_documents`, then returns the INDICES of `train_documents` that
    share NO `n`-gram with that set (the documents safe to keep).
    """
    pass

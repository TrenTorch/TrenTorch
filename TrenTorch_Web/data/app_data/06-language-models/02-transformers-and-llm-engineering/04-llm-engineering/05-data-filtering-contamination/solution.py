def get_ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def has_contamination(train_doc_tokens: list[str], eval_ngrams: set[tuple[str, ...]], n: int) -> bool:
    train_ngrams = get_ngrams(train_doc_tokens, n)
    return len(train_ngrams & eval_ngrams) > 0


def filter_contaminated_documents(
    train_documents: list[list[str]], eval_documents: list[list[str]], n: int
) -> list[int]:
    eval_ngrams: set[tuple[str, ...]] = set()
    for doc in eval_documents:
        eval_ngrams |= get_ngrams(doc, n)

    return [i for i, doc in enumerate(train_documents) if not has_contamination(doc, eval_ngrams, n)]

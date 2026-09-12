def jaccard_similarity(tokens_a: list[str], tokens_b: list[str]) -> float:
    """
    Jaccard similarity between two documents' token SETS (duplicate
    tokens within a document collapse together; only distinct tokens
    matter): `|intersection| / |union|`, `1.0` for two documents with
    an identical set of distinct tokens, `0.0` for two documents that
    share no tokens at all.
    """
    pass


def deduplicate_documents(documents: list[list[str]], threshold: float) -> list[int]:
    """
    Greedily keeps a document unless it is a NEAR-DUPLICATE (Jaccard
    similarity `>= threshold`) of a document ALREADY KEPT. Processes
    documents in order, and returns the INDICES of the kept documents
    (into the original `documents` list), in the order they were kept.
    """
    pass

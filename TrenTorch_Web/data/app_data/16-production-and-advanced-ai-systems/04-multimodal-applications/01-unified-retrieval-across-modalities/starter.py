def retrieve_across_modalities(
    chunks: list[tuple[str, str, str]], query_keywords: list[str]
) -> list[str]:
    """Each chunk is (chunk_id, modality, text) -- modality is "text" or
    "image_caption", but scoring treats them identically: this is what
    "unified" retrieval means, no special-casing by modality. Score each
    chunk by how many query_keywords (case-insensitive) appear as
    substrings of its text. Return the ids of chunks with a positive score,
    sorted by score descending, ties broken by original order. Chunks with
    zero matches are excluded entirely.
    """
    # TODO: implement
    pass

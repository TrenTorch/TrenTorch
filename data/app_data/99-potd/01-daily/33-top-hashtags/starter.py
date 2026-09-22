def top_k_hashtags(k: int, captions: list[str]) -> list[tuple[str, int]]:
    """
    The k most frequent hashtags across all captions.

    k: how many to return. captions: n caption strings; hashtags are
      whitespace-separated tokens starting with "#", other words ignored.

    Return up to k (tag, count) pairs, sorted by count descending. Ties at
    the same count are broken by earliest first appearance across the
    whole input, not alphabetically. If fewer than k distinct hashtags
    exist, return fewer than k pairs.
    """
    # TODO: record each hashtag's count and its first-appearance order,
    # then sort by (-count, first_appearance_order).
    pass

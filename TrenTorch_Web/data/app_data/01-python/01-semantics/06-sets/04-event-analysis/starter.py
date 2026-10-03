def analyze_events(batches: list) -> tuple:
    """
    `batches` is a list of event-ID lists. Each inner list contains
    the IDs observed in one dataset or batch. An ID may appear more
    than once within a batch.

    Return a 4-element tuple:

        (unique_ids, common_ids, non_common_ids, unique_count)

    where:

      - unique_ids is a LIST containing every distinct event ID
        exactly once, in the order of its first occurrence while
        scanning batches from left to right.

      - common_ids is a SET containing IDs that appear in every
        batch. Repeated occurrences within one batch count only once.

      - non_common_ids is a SET containing IDs that occur in at
        least one batch but do not occur in every batch.

      - unique_count is the number of distinct event IDs across
        all batches.

    Special cases:

      - If `batches` is empty, return ([], set(), set(), 0).

      - If `batches` contains exactly one batch, every distinct ID
        in that batch is both common and unique to that batch, so
        `common_ids` contains all distinct IDs and `non_common_ids`
        is empty.

    Requirements:

      - Do not modify `batches` or any inner list.
      - Use a set for membership tracking.
      - Use set operations to determine common and non-common IDs.
      - Use a set comprehension somewhere in the implementation
        to construct a derived set.
      - Preserve first-seen order in `unique_ids`.

    Example:

        analyze_events([
            ["a", "b", "a", "c"],
            ["b", "c", "d"],
            ["b", "c", "e"]
        ])

        -> (
            ["a", "b", "c", "d", "e"],
            {"b", "c"},
            {"a", "d", "e"},
            5
        )
    """
    pass

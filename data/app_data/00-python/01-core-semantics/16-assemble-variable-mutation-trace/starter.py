def process_batch(numbers: list, seen: list | None = None) -> dict:
    """
    Process `numbers` according to these rules, in order, using
    a for loop over `numbers`:

      - If `seen` is not provided, start with a fresh empty list
        (do not use a mutable default argument directly).
      - For each number:
          - If it's falsy (i.e. exactly 0), skip it using continue
            and do not add it to `seen`.
          - If it's negative, stop processing entirely using break
            (do not add it to `seen`, and do not process any
            numbers after it).
          - Otherwise, mutate `seen` in place by appending the
            number to it (do not reassign `seen` to a new list).

    After the loop, create a second variable `seen_alias` pointing
    at the same list object as `seen` (no copying).

    Return a dictionary:
      {
        "seen": seen,
        "seen_alias_is_same_object": <True if seen_alias and seen
                                        share the same id()>,
        "count_processed": <len of seen>
      }
    """
    pass

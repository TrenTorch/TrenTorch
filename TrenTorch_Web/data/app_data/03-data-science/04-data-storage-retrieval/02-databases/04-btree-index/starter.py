def build_index(keys: list, fanout: int) -> list:
    """
    keys: sorted list of distinct ints; fanout >= 2 entries per page.

    Returns `levels`, from the leaf level to the root. Level 0 cuts keys
    into pages of up to `fanout` keys. Each higher level has one page for
    each group of up to `fanout` consecutive pages of the level below,
    holding the smallest key of each of those child pages. The last level
    has exactly one page (the root). Empty keys give [[[]]].
    """
    # TODO: Build the leaf pages, then each level above from the one below.
    pass


def search(levels: list, key: int) -> tuple:
    """
    Descends from the root; at each non-leaf page follow the child whose
    entry is the last one <= key (the first child if key is smaller than
    all). Returns (found, pages_read) with one page read per level.
    """
    # TODO: Walk down the levels choosing a child at each page.
    pass


def range_scan(levels: list, low: int, high: int) -> tuple:
    """
    Descends to the leaf page for `low`, then reads leaf pages left to
    right until a key above `high` is seen or the leaves run out.
    Returns (keys_in_range, pages_read): pages_read counts the descent
    plus every leaf page read after the first.
    """
    # TODO: Descend once, then scan consecutive leaf pages.
    pass


def index_height(num_keys: int, fanout: int) -> int:
    """
    Returns the number of levels build_index would produce, by repeated
    division: 1 when num_keys <= fanout (including 0).
    """
    # TODO: Count how many times pages must be grouped to reach one page.
    pass

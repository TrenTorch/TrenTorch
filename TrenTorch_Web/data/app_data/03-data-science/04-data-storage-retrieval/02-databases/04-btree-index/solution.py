def build_index(keys: list, fanout: int) -> list:
    keys = list(keys)
    if not keys:
        return [[[]]]
    level = [keys[i : i + fanout] for i in range(0, len(keys), fanout)]
    levels = [level]
    while len(level) > 1:
        next_level = []
        for start in range(0, len(level), fanout):
            group = level[start : start + fanout]
            next_level.append([page[0] for page in group])
        levels.append(next_level)
        level = next_level
    return levels


def _descend(levels: list, key: int) -> tuple:
    """Returns (leaf_page_index, pages_read) for the leaf that would hold key."""
    child = 0
    for depth in range(len(levels) - 1, 0, -1):
        page = levels[depth][child]
        chosen = 0
        for position, entry in enumerate(page):
            if entry <= key:
                chosen = position
            else:
                break
        fanout_offset = child * _fanout(levels)
        child = fanout_offset + chosen
    return child, len(levels)


def _fanout(levels: list) -> int:
    # The widest page anywhere is the fanout used to build the index.
    return max(len(page) for level in levels for page in level) if levels[0][0] else 1


def search(levels: list, key: int) -> tuple:
    leaf_index, pages_read = _descend(levels, key)
    return key in levels[0][leaf_index], pages_read


def range_scan(levels: list, low: int, high: int) -> tuple:
    leaf_index, pages_read = _descend(levels, low)
    found = []
    leaves = levels[0]
    while leaf_index < len(leaves):
        for key in leaves[leaf_index]:
            if key > high:
                return found, pages_read
            if key >= low:
                found.append(key)
        leaf_index += 1
        if leaf_index < len(leaves):
            pages_read += 1
    return found, pages_read


def index_height(num_keys: int, fanout: int) -> int:
    pages = max(1, -(-num_keys // fanout))
    height = 1
    while pages > 1:
        pages = -(-pages // fanout)
        height += 1
    return height

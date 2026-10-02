def find_all(s: str, sub: str):
    """
    Return a list of the starting indices of every occurrence
    of `sub` in `s`, in increasing order, INCLUDING overlapping
    occurrences. Use find() with a moving start position.
    If `sub` is empty, return an empty list.

    Example: find_all("aaaa", "aa") -> [0, 1, 2]
    """
    pass


def count_overlapping(s: str, sub: str) -> int:
    """
    Return the number of occurrences of `sub` in `s`, counting
    overlapping occurrences. If `sub` is empty, return 0.
    Example: count_overlapping("aaaa", "aa") -> 3
             (the built-in count() would give 2)
    """
    pass


def has_extension(filename: str, ext: str) -> bool:
    """
    Return True if `filename` ends with a dot followed by `ext`,
    ignoring case. `ext` is given WITHOUT the dot.
    Example: has_extension("Report.PDF", "pdf") -> True
             has_extension("pdf", "pdf")        -> False
    """
    pass


def classify_token(token: str) -> str:
    """
    Return exactly one of the following, checked in this order:
      "digits"  if every character is a digit
      "letters" if every character is a letter
      "alnum"   if every character is a letter or digit
      "space"   if every character is whitespace
      "other"   otherwise (including the empty string)
    """
    pass

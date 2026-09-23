def classify_failures(failures: list[str], categories: dict[str, list[str]]) -> dict[str, int]:
    """`categories` maps a category name to a list of keywords. For each
    failure message, find the first category (in `categories`' insertion
    order) that has any keyword appearing as a substring of the message, and
    count it there. A failure matching no category's keywords counts under
    "UNCATEGORIZED". Return counts for every category plus "UNCATEGORIZED",
    even if some are zero.
    """
    # TODO: implement
    pass

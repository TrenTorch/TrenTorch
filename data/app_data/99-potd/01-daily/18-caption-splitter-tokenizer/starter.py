def tokenize(vocab: dict[str, int], caption: str) -> list[int]:
    """
    Split a caption on whitespace and map each word to its vocabulary id.

    vocab: word -> id. id 0 is reserved for <pad>, id 1 for <unk>.
    caption: raw text, words separated by any run of whitespace.

    Return the list of ids, one per word, in order. A word not in vocab
    maps to <unk>'s id (1). An empty (or all-whitespace) caption returns [].

    Split on any whitespace run, matching str.split() with no argument, not
    a literal single-space split.
    """
    # TODO: caption.split() with no argument already handles multiple/tab whitespace.
    pass

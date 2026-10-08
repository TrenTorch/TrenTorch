def causal_block_needed(qb, kb, bq, bk):
    """
    qb, kb: index of the query block and key block
    bq, bk: query and key block sizes

    Returns:
        True if the key block contains any position a query in block qb may attend to under causal masking.
    """
    # TODO: Compare the first key position in block kb with the last query position in block qb (see Theory).
    pass

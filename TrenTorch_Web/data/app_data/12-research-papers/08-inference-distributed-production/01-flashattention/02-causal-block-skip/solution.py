def causal_block_needed(qb, kb, bq, bk):
    return kb * bk <= qb * bq + bq - 1

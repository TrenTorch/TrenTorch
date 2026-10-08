def target_statistic(sum_y, count, prior, a=1.0):
    """
    sum_y: sum of labels seen so far for one category
    count: number of samples seen so far for that category
    prior: prior guess for the target mean
    a: weight given to the prior

    Returns:
        The smoothed mean (sum_y + a * prior) / (count + a).
    """
    # TODO: Return the prior-smoothed mean from Theory.
    pass

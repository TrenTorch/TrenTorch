def target_statistic(sum_y, count, prior, a=1.0):
    return (sum_y + a * prior) / (count + a)

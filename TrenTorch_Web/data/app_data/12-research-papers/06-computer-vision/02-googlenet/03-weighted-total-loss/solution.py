def weighted_total_loss(main, aux, w=0.3):
    return main + w * aux

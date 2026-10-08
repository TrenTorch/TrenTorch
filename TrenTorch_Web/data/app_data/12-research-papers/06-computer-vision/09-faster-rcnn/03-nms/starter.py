def nms(boxes, scores, thr):
    """
    boxes: list of [x1, y1, x2, y2] boxes
    scores: detection score of each box
    thr: IoU threshold above which a lower-scored box is suppressed

    Returns:
        Indices of the kept boxes, highest score first.
    """
    # TODO: Visit boxes from highest to lowest score, keeping a box only if it does not overlap a kept one above thr (see Theory).
    pass

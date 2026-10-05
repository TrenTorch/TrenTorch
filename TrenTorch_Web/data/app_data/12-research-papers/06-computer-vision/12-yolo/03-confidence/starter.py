def confidence(obj, iou_val):
    """
    obj: probability that the cell contains an object, in [0, 1]
    iou_val: IoU between the predicted box and the ground-truth box, in [0, 1]

    Returns:
        The confidence score obj * iou_val, a float in [0, 1].
    """
    # TODO: Multiply the object probability by the predicted box's IoU (see Theory).
    pass

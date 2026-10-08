import math


def box_targets(anchor, gt):
    ax = (anchor[0] + anchor[2]) / 2
    ay = (anchor[1] + anchor[3]) / 2
    aw = anchor[2] - anchor[0]
    ah = anchor[3] - anchor[1]
    gx = (gt[0] + gt[2]) / 2
    gy = (gt[1] + gt[3]) / 2
    gw = gt[2] - gt[0]
    gh = gt[3] - gt[1]
    return ((gx - ax) / aw, (gy - ay) / ah, math.log(gw / aw), math.log(gh / ah))

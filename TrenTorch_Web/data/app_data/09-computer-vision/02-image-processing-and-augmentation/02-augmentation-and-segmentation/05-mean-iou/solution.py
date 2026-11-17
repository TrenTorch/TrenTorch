import numpy as np


def confusion_matrix(pred, target, n_classes):
    idx = np.asarray(target).ravel().astype(int) * n_classes + np.asarray(pred).ravel().astype(int)
    return np.bincount(idx, minlength=n_classes * n_classes).reshape(n_classes, n_classes)


def mean_iou(conf):
    conf = np.asarray(conf, dtype=float)
    tp = np.diag(conf)
    denom = conf.sum(axis=1) + conf.sum(axis=0) - tp
    ious = np.full(len(tp), np.nan)
    ok = denom > 0
    ious[ok] = tp[ok] / denom[ok]
    return float(np.nanmean(ious)), ious

import numpy as np


def class_distribution(labels, n_classes):
    labels = np.asarray(labels)
    counts = np.bincount(labels, minlength=n_classes)
    return counts / len(labels)

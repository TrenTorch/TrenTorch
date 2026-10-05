import numpy as np


def _gram(feat):
    C = feat.shape[0]
    F = np.asarray(feat, dtype=float).reshape(C, -1)
    return F @ F.T / F.size


def content_loss(gen_feat, content_feat):
    return float(np.mean((np.asarray(gen_feat, dtype=float) - np.asarray(content_feat, dtype=float)) ** 2))


def style_loss(gen_feats, style_feats, layer_weights):
    return float(sum(w * np.mean((_gram(g) - _gram(s)) ** 2) for g, s, w in zip(gen_feats, style_feats, layer_weights)))


def total_loss(content, style, tv, w_content, w_style, w_tv):
    return float(w_content * content + w_style * style + w_tv * tv)

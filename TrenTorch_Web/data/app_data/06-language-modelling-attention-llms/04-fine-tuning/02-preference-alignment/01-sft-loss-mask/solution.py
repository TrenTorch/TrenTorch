import numpy as np


def response_mask(prompt_lens, seq_lens, T):
    t = np.arange(T)[None, :]
    return (t >= np.asarray(prompt_lens)[:, None]) & (t < np.asarray(seq_lens)[:, None])


def sft_loss(logits, token_ids, prompt_lens, seq_lens):
    B, T, V = logits.shape
    mask = response_mask(prompt_lens, seq_lens, T)[:, 1:]
    z = logits[:, :-1]
    z = z - z.max(axis=-1, keepdims=True)
    logp = z - np.log(np.exp(z).sum(axis=-1, keepdims=True))
    targets = token_ids[:, 1:]
    picked = np.take_along_axis(logp, targets[..., None], axis=-1)[..., 0]
    return float(-(picked * mask).sum() / mask.sum())

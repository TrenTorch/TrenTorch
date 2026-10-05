import numpy as np


def lda_estimates(doc_topic: np.ndarray, topic_word: np.ndarray, alpha: float, beta: float):
    doc_topic = np.asarray(doc_topic, dtype=float)
    topic_word = np.asarray(topic_word, dtype=float)
    if doc_topic.ndim != 2 or topic_word.ndim != 2:
        raise ValueError("doc_topic and topic_word must be 2-D")
    D, K = doc_topic.shape
    K2, V = topic_word.shape
    if K != K2:
        raise ValueError("doc_topic and topic_word disagree on the number of topics")
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive")
    if np.any(doc_topic < 0) or np.any(topic_word < 0):
        raise ValueError("counts must be nonnegative")
    theta = (doc_topic + alpha) / (doc_topic.sum(axis=1, keepdims=True) + K * alpha)
    phi = (topic_word + beta) / (topic_word.sum(axis=1, keepdims=True) + V * beta)
    return theta, phi

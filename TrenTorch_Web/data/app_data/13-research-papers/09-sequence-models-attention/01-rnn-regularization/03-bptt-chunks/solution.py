import math


def bptt_chunks(T, bptt):
    return math.ceil(T / bptt)

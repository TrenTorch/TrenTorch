from collections import Counter


def get_pair_frequencies(corpus: list[list[str]]) -> Counter:
    pair_counts = Counter()
    for sequence in corpus:
        for i in range(len(sequence) - 1):
            pair_counts[(sequence[i], sequence[i + 1])] += 1
    return pair_counts


def merge_pair(corpus: list[list[str]], pair: tuple[str, str]) -> list[list[str]]:
    merged_token = pair[0] + pair[1]
    new_corpus = []
    for sequence in corpus:
        new_sequence = []
        i = 0
        while i < len(sequence):
            if i < len(sequence) - 1 and (sequence[i], sequence[i + 1]) == pair:
                new_sequence.append(merged_token)
                i += 2
            else:
                new_sequence.append(sequence[i])
                i += 1
        new_corpus.append(new_sequence)
    return new_corpus


def bpe_single_merge_step(corpus: list[list[str]]) -> tuple[list[list[str]], tuple[str, str]]:
    pair_counts = get_pair_frequencies(corpus)
    most_frequent_pair = max(pair_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
    new_corpus = merge_pair(corpus, most_frequent_pair)
    return new_corpus, most_frequent_pair

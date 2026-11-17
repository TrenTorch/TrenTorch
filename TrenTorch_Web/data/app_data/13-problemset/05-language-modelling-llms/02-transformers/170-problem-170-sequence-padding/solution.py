import numpy as np

def solve(sequences, pad_value=0):
    """Right-pad variable-length sequences and return the padded batch and lengths."""
    sequences = [list(sequence) for sequence in sequences]
    lengths = np.asarray([len(sequence) for sequence in sequences], dtype=int)
    width = int(lengths.max()) if len(lengths) else 0
    padded = np.full((len(sequences), width), pad_value)
    for row, sequence in enumerate(sequences):
        padded[row, :len(sequence)] = sequence
    return padded, lengths

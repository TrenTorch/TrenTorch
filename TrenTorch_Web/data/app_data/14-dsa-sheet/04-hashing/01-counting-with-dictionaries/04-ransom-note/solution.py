from collections import Counter


def ransom_note(note, magazine):
    return not (Counter(note) - Counter(magazine))
